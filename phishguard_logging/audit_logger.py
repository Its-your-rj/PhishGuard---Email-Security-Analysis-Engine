import logging
import json
import os
from datetime import datetime
from pathlib import Path

class AuditLogger:
    """Advanced logging and audit system for PhishGuard"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create different log files
        self.classification_log = self.log_dir / "classifications.log"
        self.audit_log = self.log_dir / "audit.log"
        self.error_log = self.log_dir / "errors.log"
        self.decision_log = self.log_dir / "decisions.json"
        
        # Set up loggers
        self.classification_logger = self._setup_logger(
            "classification",
            self.classification_log
        )
        self.audit_logger = self._setup_logger(
            "audit",
            self.audit_log
        )
        self.error_logger = self._setup_logger(
            "error",
            self.error_log
        )
        
        # Initialize decision log
        if not self.decision_log.exists():
            with open(self.decision_log, 'w') as f:
                json.dump([], f)
    
    def _setup_logger(self, name, log_file):
        """Setup logger with file handler"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def log_classification(self, email_file, classification, confidence, 
                          sender=None, subject=None):
        """Log email classification"""
        message = (
            f"Email: {email_file} | "
            f"Classification: {classification} | "
            f"Confidence: {confidence:.2f} | "
            f"Sender: {sender} | "
            f"Subject: {subject}"
        )
        self.classification_logger.info(message)
        
        # Also save to JSON for analytics
        self._add_to_decision_log(
            email_file, classification, confidence, sender, subject
        )
    
    def log_user_action(self, user, action, details):
        """Log user actions in the system"""
        message = f"User: {user} | Action: {action} | Details: {details}"
        self.audit_logger.info(message)
    
    def log_decision_details(self, email_file, classification, 
                            phishing_score, spam_score, indicators):
        """Log detailed classification decision to text log only"""
        decision_text = (
            f"Email: {email_file} | "
            f"Classification: {classification} | "
            f"Phishing Score: {phishing_score:.2f} | "
            f"Spam Score: {spam_score:.2f} | "
            f"Indicators: {', '.join(indicators)}"
        )
        self.audit_logger.info(decision_text)
    
    def log_error(self, error_type, error_message, context=None):
        """Log errors"""
        message = f"Error Type: {error_type} | Message: {error_message}"
        if context:
            message += f" | Context: {context}"
        self.error_logger.error(message)
    
    def _add_to_decision_log(self, email_file, classification, 
                            confidence, sender, subject):
        """Add classification to decision log"""
        decision = {
            "timestamp": datetime.now().isoformat(),
            "email": str(email_file),
            "classification": classification,
            "confidence": float(confidence),
            "sender": sender,
            "subject": subject
        }
        self._save_decision(decision)
    
    def _save_decision(self, decision):
        """Save decision to JSON log"""
        try:
            with open(self.decision_log, 'r') as f:
                decisions = json.load(f)
        except:
            decisions = []
        
        decisions.append(decision)
        
        with open(self.decision_log, 'w') as f:
            json.dump(decisions, f, indent=2)
    
    def get_classification_history(self, limit=100):
        """Get recent classifications"""
        try:
            with open(self.decision_log, 'r') as f:
                decisions = json.load(f)
            return decisions[-limit:]
        except:
            return []
    
    def get_statistics(self):
        """Get classification statistics"""
        try:
            with open(self.decision_log, 'r') as f:
                decisions = json.load(f)
        except:
            return {}
        
        if not decisions:
            return {
                "total": 0,
                "phishing": 0,
                "spam": 0,
                "ham": 0,
                "phishing_percentage": 0,
                "spam_percentage": 0,
                "ham_percentage": 0
            }
        
        total = len(decisions)
        phishing = sum(1 for d in decisions if d['classification'] == 'PHISHING')
        spam = sum(1 for d in decisions if d['classification'] == 'SPAM')
        ham = sum(1 for d in decisions if d['classification'] == 'HAM')
        
        return {
            "total": total,
            "phishing": phishing,
            "spam": spam,
            "ham": ham,
            "phishing_percentage": (phishing / total * 100) if total > 0 else 0,
            "spam_percentage": (spam / total * 100) if total > 0 else 0,
            "ham_percentage": (ham / total * 100) if total > 0 else 0
        }
    
    def generate_compliance_report(self):
        """Generate compliance report"""
        stats = self.get_statistics()
        history = self.get_classification_history()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": stats,
            "recent_classifications": history[-50:],
            "classification_logs": str(self.classification_log),
            "audit_logs": str(self.audit_log),
            "error_logs": str(self.error_log)
        }
        
        return report
    
    def clear_all_data(self):
        """Clear all analysis data and logs"""
        try:
            # Clear decision log
            with open(self.decision_log, 'w') as f:
                json.dump([], f)
            
            # Clear classification log
            with open(self.classification_log, 'w') as f:
                f.write('')
            
            # Clear audit log
            with open(self.audit_log, 'w') as f:
                f.write('')
            
            # Clear error log
            with open(self.error_log, 'w') as f:
                f.write('')
            
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
