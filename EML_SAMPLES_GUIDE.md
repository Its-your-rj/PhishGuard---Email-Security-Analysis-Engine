# 📧 Sample EML Files - Complete Collection

You now have **13 sample EML files** ready to download and test in PhishGuard!

## 📁 File Locations

All files are in: `e:\projectpcr\samples\`

### 🚨 Phishing Samples (6 files)
1. **phishing_bank.eml** - Bank of America alert scam
2. **phishing_amazon.eml** - Amazon account verification scam
3. **phishing_paypal.eml** - PayPal payment issue scam
4. **phishing_paypal2.eml** - PayPal billing update scam
5. **phishing_microsoft.eml** - Microsoft/Office 365 security scam
6. **phishing_spoofed.eml** - Corporate email spoofing

### ⚠️ Spam Samples (2 files)
1. **spam_offer.eml** - Lottery/prize scam
2. **spam_software.eml** - Software discount scam

### ✅ Legitimate Samples (4 files)
1. **ham_legitimate.eml** - Company meeting memo
2. **legitimate_work.eml** - HR performance review
3. **legitimate_amazon.eml** - Amazon order shipment
4. **legitimate_github.eml** - GitHub security alert

---

## 🎯 How to Download & Use

### Method 1: Using File Explorer
1. Open Windows File Explorer
2. Navigate to: `E:\projectpcr\samples\`
3. Right-click any `.eml` file
4. Choose "Copy"
5. Paste wherever you need it

### Method 2: Using PhishGuard Dashboard
1. Open http://localhost:5000
2. Go to "Analyze Email" 
3. Click "Choose File"
4. Browse to `E:\projectpcr\samples\`
5. Select an `.eml` file
6. Click "Open" then "Analyze"

### Method 3: Command Line
```powershell
# Copy a specific file
Copy-Item "E:\projectpcr\samples\phishing_bank.eml" -Destination "C:\Users\YourName\Downloads\"

# Copy all samples
Copy-Item "E:\projectpcr\samples\*.eml" -Destination "C:\Users\YourName\Downloads\"
```

---

## 📊 Quick Reference Table

| File | Type | Category | Expected Result |
|------|------|----------|-----------------|
| phishing_bank.eml | Bank alert | Phishing | 🚨 PHISHING |
| phishing_amazon.eml | Amazon security | Phishing | 🚨 PHISHING |
| phishing_paypal.eml | PayPal billing | Phishing | 🚨 PHISHING |
| phishing_paypal2.eml | PayPal payment | Phishing | 🚨 PHISHING |
| phishing_microsoft.eml | Office 365 alert | Phishing | 🚨 PHISHING |
| phishing_spoofed.eml | Domain spoof | Phishing | 🚨 PHISHING |
| spam_offer.eml | Lottery scam | Spam | ⚠️ SPAM |
| spam_software.eml | Software sale | Spam | ⚠️ SPAM |
| ham_legitimate.eml | Company memo | Legitimate | ✅ LEGITIMATE |
| legitimate_work.eml | HR notification | Legitimate | ✅ LEGITIMATE |
| legitimate_amazon.eml | Order shipped | Legitimate | ✅ LEGITIMATE |
| legitimate_github.eml | GitHub alert | Legitimate | ✅ LEGITIMATE |

---

## 💡 Testing Tips

### For Quick Testing:
Start with these 3 files:
- `spam_offer.eml` (obvious spam)
- `phishing_bank.eml` (obvious phishing)
- `ham_legitimate.eml` (obvious legitimate)

### For Comprehensive Testing:
Analyze all 13 files in order:
1. Spam samples (easy to detect)
2. Legitimate samples (should pass)
3. Phishing samples (the real challenge)

### Verify Results:
After analyzing, check:
- ✓ Correct classification
- ✓ High confidence score
- ✓ Clear indicators/reasons
- ✓ Statistics updated on dashboard
- ✓ Entry in History page

---

## 🔧 What Each File Demonstrates

### Phishing Detection Tests:
- **phishing_bank.eml**: Detects banking threats
- **phishing_amazon.eml**: Detects ecommerce scams
- **phishing_paypal.eml/paypal2.eml**: Detects payment scams
- **phishing_microsoft.eml**: Detects enterprise software scams
- **phishing_spoofed.eml**: Detects domain spoofing

### Spam Detection Tests:
- **spam_offer.eml**: Detects lottery/prize scams
- **spam_software.eml**: Detects unrealistic offers

### Legitimate Email Tests:
- **ham_legitimate.eml**: Company emails
- **legitimate_work.eml**: HR communications
- **legitimate_amazon.eml**: Real ecommerce confirmations
- **legitimate_github.eml**: Real service alerts

---

## 📝 File Format

All files are standard **EML (Email) format**:
- Plain text files
- Contains email headers (From, To, Subject, Date, etc.)
- Contains email body (HTML or plain text)
- Fully RFC-compliant
- Safe to open and analyze

---

## ✅ Ready to Test!

You have everything you need. Just:
1. Download any EML file
2. Upload to PhishGuard Analyze page
3. Review the classification results
4. Check the dashboard statistics

**Happy testing! 🛡️**
