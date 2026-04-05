# PhishGuard Email Security Analysis Engine - Setup and Run Guide

## Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS

## Quick Start

### 1. Install Dependencies
```bash
# Navigate to the project directory
cd PhishGuard---Email-Security-Analysis-Engine

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run the Web Dashboard
```bash
# Navigate to the web directory
cd phishguard_web

# Start the Flask application
python app.py
```

### 3. Access the Dashboard
Open your web browser and go to: `http://localhost:5000`

## Detailed Setup

### Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Directory Structure
```
PhishGuard---Email-Security-Analysis-Engine/
├── phishguard_web/          # Web dashboard
│   ├── app.py               # Main Flask application
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── classifier.py            # Email classification logic
├── email_parser.py          # Email parsing utilities
├── phishguard_logging/      # Logging and audit system
├── phishguard_ml/           # Machine learning models
├── samples/                 # Sample email files for testing
└── requirements.txt         # Python dependencies
```

## Features

### Dashboard Navigation
- **Dashboard**: Overview of analysis statistics and system status
- **Analyze**: Upload and analyze email files (.eml format)
- **History**: View recent classification results
- **Statistics**: Detailed analytics and trends
- **Settings**: Configure analysis parameters
- **Compliance**: Audit reports and compliance metrics

### Email Analysis
1. Upload an .eml file through the web interface
2. The system performs multi-layered analysis:
   - Header authentication (SPF, DKIM, DMARC)
   - Content analysis for phishing patterns
   - Machine learning classification
   - Rule-based heuristics
3. Results show classification, confidence score, and threat indicators

### Sample Emails
Test the system with sample emails in the `samples/` directory:
- `phishing_*.eml` - Phishing email examples
- `legitimate_*.eml` - Safe email examples
- `spam_*.eml` - Spam email examples

## API Endpoints

### Analysis
- `POST /analyze` - Analyze uploaded email file
- `GET /api/stats` - Get system statistics
- `GET /api/history` - Get classification history

### Management
- `GET/POST /api/settings` - Get/update system settings
- `POST /api/clear-data` - Clear all analysis data
- `GET /api/export-report` - Export compliance report

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

2. **Template Not Found**
   - Ensure you're running from the `phishguard_web` directory
   - Check that all template files exist in `templates/` folder

3. **Port Already in Use**
   - Change the port in `app.py`: `app.run(port=5001)`

4. **File Upload Issues**
   - Ensure uploaded files are valid .eml format
   - Check file size limits (16MB default)

### Logs
- Classification logs: `phishguard_web/logs/classifications.log`
- Error logs: `phishguard_web/logs/errors.log`
- Audit logs: `phishguard_web/logs/audit.log`

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
```

## Security Notes
- The application runs in debug mode by default
- For production deployment, set `debug=False` in `app.py`
- Configure proper authentication and authorization for production use
- Regularly update dependencies for security patches

## Support
For issues or questions, check the logs in the `logs/` directory or review the code documentation in each module.