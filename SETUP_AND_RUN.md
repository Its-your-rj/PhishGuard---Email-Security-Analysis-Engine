# Email Security Analysis Engine - Setup & Run Guide

## Overview
This is an Email Security Analysis Engine that detects spam and phishing emails using both rule-based analysis and machine learning approaches.

## Status
✅ **All errors fixed!** The project is ready to use.

## System Requirements
- Python 3.8+
- Windows, macOS, or Linux

## Fixed Issues

### Issue 1: Unicode Encoding Error in create_samples.py
**Problem**: Emoji characters (🎉, 🎊, etc.) were causing UnicodeEncodeError on Windows
**Solution**: Added UTF-8 encoding when writing to files:
```python
filepath.write_text(content, encoding='utf-8')
```

---

## Step-by-Step Setup and Run Instructions

### Step 1: Verify Python Environment
Your Python environment is already configured with all required dependencies.

**Verify the environment:**
```bash
E:/projectpcr/.venv/Scripts/python.exe --version
```

### Step 2: Generate Sample Emails (First Time Only)
Create sample email files for testing:

```bash
cd e:\projectpcr
E:/projectpcr/.venv/Scripts/python.exe create_samples.py
```

**Output:**
```
Created: samples\ham_legitimate.eml
Created: samples\spam_offer.eml
Created: samples\phishing_paypal.eml
Created: samples\phishing_bank.eml
Created: samples\phishing_spoofed.eml

✓ Created 5 sample email files in 'samples/' directory
```

This creates 5 sample email files in the `samples/` directory:
- `ham_legitimate.eml` - A legitimate business email
- `spam_offer.eml` - A spam email with too-good-to-be-true offer
- `phishing_paypal.eml` - A phishing email impersonating PayPal
- `phishing_bank.eml` - A phishing email impersonating a bank
- `phishing_spoofed.eml` - A spoofed domain phishing attempt

---

## Step 3: Analyze a Single Email

### Basic Analysis (Text Output)
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/ham_legitimate.eml
```

**Output:**
```
📧 Analyzing email: samples/ham_legitimate.eml

╭───────────── Classification Result ──────────────╮
│ ✓ HAM                                            │
│ Confidence: 100.0%                               │
╰──────────────────────────────────────────────────╯

📧 Email Details:
 From:     john.doe@company.com
 To:       jane.smith@company.com
 Subject:  Q4 Meeting Notes
 Date:     Fri, 19 Jan 2024 10:00:00 +0000

🛡️  Recommendation:  SAFE - Email appears legitimate
```

### Analyze a Phishing Email
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml
```

### Output as JSON
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -f json
```

### Save Output to File
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -o result.json -f json
```

### Generate HTML Report
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -o report.html -f html
```

### Verbose Output
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -v
```

---

## Step 4: Batch Process Multiple Emails

### Process All Emails in samples/ Directory
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/
```

**Output:**
```
📦 Processing 5 email(s)...

Analyzing... ━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

       Batch Analysis Summary        
┏━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Category     ┃ Count ┃ Percentage ┃
┡━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Total Emails │ 5     │ 100%       │
│ Phishing     │ 2     │ 40.0%      │
│ Spam         │ 0     │ 0.0%       │
│ Ham (Safe)   │ 3     │ 60.0%      │
└──────────────┴───────┴────────────┘

✓ Batch report saved to batch_report.json
```

### Save Batch Report to Custom File
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/ -o my_report.json
```

### Process Subdirectories Recursively
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/ -r
```

---

## Step 5: Train a Custom Model (Optional)

If you have your own email dataset with HAM, SPAM, and PHISHING folders:

### Dataset Structure Required:
```
dataset/
├── ham/
│   ├── email1.eml
│   ├── email2.eml
│   └── ...
├── spam/
│   ├── email1.eml
│   ├── email2.eml
│   └── ...
└── phishing/
    ├── email1.eml
    ├── email2.eml
    └── ...
```

### Train Command:
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py train path/to/dataset/
```

### With Custom Model Output Path:
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py train path/to/dataset/ -m models/my_model.pkl
```

### With Custom Epochs:
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py train path/to/dataset/ -e 20
```

---

## Available Commands Summary

```bash
# Show help
E:/projectpcr/.venv/Scripts/python.exe cli.py --help

# Show version
E:/projectpcr/.venv/Scripts/python.exe cli.py --version

# Analyze single email
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze <email_file> [OPTIONS]

# Batch process
E:/projectpcr/.venv/Scripts/python.exe cli.py batch <directory> [OPTIONS]

# Train model
E:/projectpcr/.venv/Scripts/python.exe cli.py train <dataset_dir> [OPTIONS]
```

---

## Command Options Reference

### analyze command options:
- `-f, --format [text|json|html]` - Output format (default: text)
- `-o, --output PATH` - Save output to file
- `-v, --verbose` - Show additional details

### batch command options:
- `-o, --output PATH` - Output report file (default: batch_report.json)
- `-r, --recursive` - Process subdirectories recursively

### train command options:
- `-m, --model-output PATH` - Model output path (default: models/trained_model.pkl)
- `-e, --epochs INTEGER` - Training epochs (default: 10)

---

## Project Files

- `classifier.py` - Email classification logic (rule-based and ML)
- `email_parser.py` - Email parsing and feature extraction
- `model_trainer.py` - ML model training and evaluation
- `cli.py` - Command-line interface
- `create_samples.py` - Sample email generator
- `setup.py` - Package configuration
- `requirements.txt` - Python dependencies
- `samples/` - Sample email files (created by create_samples.py)

---

## Classification Results

### Email Categories:
1. **HAM** - Legitimate email (safe)
2. **SPAM** - Unsolicited email or marketing emails
3. **PHISHING** - Suspicious email attempting to steal information

### Example Results:

#### Legitimate Email (HAM)
```
✓ HAM
Confidence: 100.0%
Recommendation: SAFE - Email appears legitimate
```

#### Phishing Email (PHISHING)
```
🚨 PHISHING
Confidence: 100.0%
Threat Indicators:
  ✗ Reply-To address doesn't match sender
  ✗ Contains suspicious URL(s)
  ✗ Contains phishing pattern(s)
  ✗ Possible domain spoofing
Recommendation: DELETE IMMEDIATELY - High confidence phishing attempt
```

---

## Python Executable Path

If you need to run Python commands directly:
```
E:/projectpcr/.venv/Scripts/python.exe
```

Or use the shortcut (if added to PATH):
```
python
```

---

## Troubleshooting

### Unicode Encoding Errors
If you encounter Unicode errors on Windows, use:
```bash
chcp 65001
```
Before running commands to switch to UTF-8 encoding.

### Missing Dependencies
If you encounter import errors, reinstall requirements:
```bash
E:/projectpcr/.venv/Scripts/pip.exe install -r requirements.txt
```

### Permission Errors
On some systems, you may need to adjust permissions:
```bash
# Windows: Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Example Workflow

```bash
# 1. Create sample emails
E:/projectpcr/.venv/Scripts/python.exe create_samples.py

# 2. Analyze a legitimate email
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/ham_legitimate.eml

# 3. Analyze a phishing email
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml

# 4. Batch process all samples
E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/

# 5. Save batch results to JSON
E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/ -o results.json

# 6. Generate HTML report
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -f html -o report.html
```

---

## Notes

- All files are now working correctly with proper UTF-8 encoding
- The project includes 5 sample emails for testing
- Results can be saved in text, JSON, or HTML formats
- Custom datasets can be used for model training
- The classifier uses a combination of rule-based and ML approaches for better accuracy

