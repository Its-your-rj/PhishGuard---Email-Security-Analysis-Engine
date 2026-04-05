# PhishGuard Email Security Analysis Engine - Quick Start Guide

## 🚀 Quick Launch

### Option 1: Simple Start (Recommended)
```bash
python run.py
```

### Option 2: Manual Start
```bash
cd phishguard_web
python app.py
```

## 📋 What Happens Next

1. **Server Starts**: Flask development server launches on `http://localhost:5000`
2. **Dashboard Loads**: Professional web interface with all features connected
3. **Real-time Updates**: Statistics and activity update automatically
4. **Full Functionality**: All analysis, logging, and reporting features work

## 🎯 Dashboard Features

### Navigation Menu
- **Dashboard**: Real-time statistics and recent activity
- **Analyze**: Upload .eml files for security analysis
- **History**: Complete log of all email classifications
- **Statistics**: Interactive charts and trends
- **Settings**: Configure analysis parameters
- **Compliance**: Audit reports and compliance metrics

### Key Features Working
- ✅ Email file upload and parsing
- ✅ Multi-layered security analysis (SPF, DKIM, DMARC + ML)
- ✅ Real-time dashboard with auto-refresh
- ✅ Professional UI with loading indicators
- ✅ Comprehensive logging and audit trails
- ✅ Interactive charts and statistics
- ✅ Settings management
- ✅ Compliance reporting

## 🧪 Test the System

1. **Upload Sample Emails**: Use files from `samples/` directory
2. **View Results**: See classifications, confidence scores, and indicators
3. **Check Dashboard**: Statistics update automatically
4. **Explore Features**: Try all navigation sections

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## 🔧 Troubleshooting

- **Port 5000 busy**: Server will tell you if port is in use
- **Import errors**: Ensure dependencies are installed with `pip install -r requirements.txt`
- **File upload issues**: Only .eml files are supported
- **Charts not loading**: Ensure internet connection for Chart.js CDN

## 📊 System Status

The dashboard shows:
- Total emails analyzed
- Phishing/spam/ham detection counts
- System uptime
- Recent activity feed
- Real-time statistics updates

Everything is now properly connected and working seamlessly!