from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import io

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classifier import EmailClassifier
from email_parser import EmailParser
from phishguard_logging.audit_logger import AuditLogger
from phishguard_ml.enhanced_model import EnhancedMLModel

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
classifier = EmailClassifier()
email_parser = EmailParser()
audit_logger = AuditLogger()
ml_model = EnhancedMLModel()

# Store uploaded files temporarily
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

class DashboardStats:
    """Track dashboard statistics"""
    def __init__(self):
        self.total_analyzed = 0
        self.start_time = datetime.now()
    
    def get_uptime(self):
        delta = datetime.now() - self.start_time
        hours = delta.total_seconds() / 3600
        return f"{hours:.1f} hours"

dashboard_stats = DashboardStats()

# Routes

@app.route('/')
def index():
    """Main dashboard page"""
    stats = audit_logger.get_statistics()
    stats['uptime'] = dashboard_stats.get_uptime()
    return render_template('dashboard.html', stats=stats)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Email analysis page"""
    if request.method == 'POST':
        if 'email_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['email_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save and analyze
        filepath = UPLOAD_FOLDER / file.filename
        file.save(filepath)
        
        try:
            # Parse email file
            parsed_email = email_parser.parse_file(str(filepath))
            
            # Classify
            result = classifier.classify(parsed_email)
            
            # Log classification
            audit_logger.log_classification(
                email_file=file.filename,
                classification=result['classification'],
                confidence=result['confidence'],
                sender=parsed_email.get('from', 'Unknown'),
                subject=parsed_email.get('subject', '(No subject)')
            )
            
            # Log detailed decision
            audit_logger.log_decision_details(
                email_file=file.filename,
                classification=result['classification'],
                phishing_score=result.get('rule_score', 0),
                spam_score=result.get('ml_score', 0),
                indicators=result.get('threat_indicators', [])
            )
            
            # Clean up
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'classification': result['classification'],
                'confidence': result['confidence'],
                'indicators': result.get('threat_indicators', []),
                'recommendation': result.get('recommendation', '')
            })
        
        except Exception as e:
            audit_logger.log_error('ANALYSIS_ERROR', str(e), file.filename)
            return jsonify({'error': str(e)}), 500
    
    return render_template('analyze.html')

@app.route('/history')
def history():
    """Classification history page"""
    history = audit_logger.get_classification_history(200)
    return render_template('history.html', history=history)

@app.route('/statistics')
def statistics():
    """Statistics and trends page"""
    stats = audit_logger.get_statistics()
    history = audit_logger.get_classification_history(500)
    
    # Calculate trends
    trends = {
        'daily': calculate_daily_trends(history),
        'hourly': calculate_hourly_trends(history)
    }
    
    return render_template('statistics.html', stats=stats, trends=trends)

@app.route('/settings')
def settings():
    """Settings page"""
    settings_data = {
        'phishing_threshold': 0.40,
        'spam_threshold': 0.35,
        'ml_enabled': ml_model.is_trained,
        'use_ensemble': True
    }
    return render_template('settings.html', settings=settings_data)

@app.route('/compliance')
def compliance():
    """Compliance and audit page"""
    report = audit_logger.generate_compliance_report()
    return render_template('compliance.html', report=report)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = audit_logger.get_statistics()
    return jsonify(stats)

@app.route('/api/history')
def api_history():
    """API endpoint for history"""
    limit = request.args.get('limit', 100, type=int)
    history = audit_logger.get_classification_history(limit)
    return jsonify(history)

@app.route('/api/export-report')
def export_report():
    """Export compliance report"""
    report = audit_logger.generate_compliance_report()
    
    # Create downloadable JSON
    json_data = json.dumps(report, indent=2)
    
    return send_file(
        io.BytesIO(json_data.encode()),
        mimetype='application/json',
        as_attachment=True,
        download_name=f"phishguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

@app.route('/api/clear-data', methods=['POST'])
def clear_data():
    """Clear all analysis data"""
    success = audit_logger.clear_all_data()
    if success:
        return jsonify({'success': True, 'message': 'All data cleared successfully'})
    else:
        return jsonify({'success': False, 'message': 'Error clearing data'}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    """API for settings management"""
    if request.method == 'POST':
        settings = request.json
        
        # Log setting changes
        audit_logger.log_user_action(
            'system',
            'SETTINGS_CHANGED',
            json.dumps(settings)
        )
        
        return jsonify({'success': True, 'message': 'Settings updated'})
    
    settings_data = {
        'phishing_threshold': 0.40,
        'spam_threshold': 0.35,
        'ml_enabled': ml_model.is_trained,
        'use_ensemble': True
    }
    return jsonify(settings_data)

# Helper functions

def calculate_daily_trends(history):
    """Calculate daily classification trends"""
    from collections import defaultdict
    
    daily = defaultdict(lambda: {'phishing': 0, 'spam': 0, 'ham': 0})
    
    for record in history:
        date = record['timestamp'].split('T')[0]
        classification = record['classification'].lower()
        daily[date][classification] += 1
    
    return dict(daily)

def calculate_hourly_trends(history):
    """Calculate hourly classification trends"""
    from collections import defaultdict
    
    hourly = defaultdict(lambda: {'phishing': 0, 'spam': 0, 'ham': 0})
    
    for record in history:
        hour = record['timestamp'].split('T')[1][:2]
        classification = record['classification'].lower()
        hourly[hour][classification] += 1
    
    return dict(hourly)

if __name__ == '__main__':
    print("Starting PhishGuard Web Dashboard")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
