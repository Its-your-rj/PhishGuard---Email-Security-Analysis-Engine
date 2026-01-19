# Quick Start Guide

## ⚡ 30-Second Setup

### 1. Generate Sample Emails
```bash
E:/projectpcr/.venv/Scripts/python.exe create_samples.py
```

### 2. Analyze an Email
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml
```

### 3. Batch Process
```bash
E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/
```

---

## Common Commands

| Task | Command |
|------|---------|
| **Analyze email** | `E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/ham_legitimate.eml` |
| **Analyze as JSON** | `E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -f json` |
| **Save to file** | `E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -o result.json -f json` |
| **Generate HTML** | `E:/projectpcr/.venv/Scripts/python.exe cli.py analyze samples/phishing_paypal.eml -f html -o report.html` |
| **Batch process** | `E:/projectpcr/.venv/Scripts/python.exe cli.py batch samples/ -o report.json` |
| **Show help** | `E:/projectpcr/.venv/Scripts/python.exe cli.py --help` |

---

## Test Files Included

✅ `ham_legitimate.eml` - Safe business email
⚠️  `spam_offer.eml` - Spam email  
🚨 `phishing_paypal.eml` - PayPal phishing
🚨 `phishing_bank.eml` - Bank phishing
🚨 `phishing_spoofed.eml` - Spoofed domain phishing

---

## Full Documentation

See `SETUP_AND_RUN.md` for complete setup and usage instructions.
