# 📧 EML Sample Files - Download Complete

## ✅ What You Have

You now have **13 real-world EML sample files** organized in 3 categories:

### 📁 Location: `E:\projectpcr\samples\`

```
samples/
├── 🚨 PHISHING (6 files)
│   ├── phishing_bank.eml
│   ├── phishing_amazon.eml
│   ├── phishing_paypal.eml
│   ├── phishing_paypal2.eml
│   ├── phishing_microsoft.eml
│   └── phishing_spoofed.eml
│
├── ⚠️ SPAM (2 files)
│   ├── spam_offer.eml
│   └── spam_software.eml
│
├── ✅ LEGITIMATE (4 files)
│   ├── ham_legitimate.eml
│   ├── legitimate_work.eml
│   ├── legitimate_amazon.eml
│   └── legitimate_github.eml
│
└── 📖 Documentation
    ├── README.md (detailed testing guide)
    ├── Copy_Samples_To_Downloads.bat (easy copy script)
    └── EML_SAMPLES_GUIDE.md (in root folder)
```

---

## 🎯 Quick Start

### Option 1: Easiest - Using PhishGuard Dashboard
1. Open http://localhost:5000
2. Click "Analyze Email"
3. Click "Choose File"
4. Navigate to `E:\projectpcr\samples\`
5. Select any `.eml` file
6. Click "Analyze"

### Option 2: Copy to Downloads First
1. Open `E:\projectpcr\samples\`
2. Right-click `Copy_Samples_To_Downloads.bat`
3. Click "Run as administrator"
4. All files will copy to your Downloads folder
5. Then upload from Downloads in PhishGuard

### Option 3: Manual Copy
- Press `Win + E` to open File Explorer
- Navigate to `E:\projectpcr\samples\`
- Select files you want (use Ctrl+Click for multiple)
- Right-click → Copy
- Paste wherever needed

---

## 📊 What Each Sample Demonstrates

### 🚨 PHISHING (6 samples) - Credential Theft Attempts
| File | Target | Method |
|------|--------|--------|
| phishing_bank.eml | Bank of America | Fake security alert |
| phishing_amazon.eml | Amazon | Locked account warning |
| phishing_paypal.eml | PayPal | Failed payment notification |
| phishing_paypal2.eml | PayPal | Payment update request |
| phishing_microsoft.eml | Office 365 | Unusual sign-in alert |
| phishing_spoofed.eml | Corporate | Domain impersonation |

### ⚠️ SPAM (2 samples) - Unwanted Commercial/Scam
| File | Type | Tactic |
|------|------|--------|
| spam_offer.eml | Lottery | "You've won $1 million" |
| spam_software.eml | Discount | "90% off software" |

### ✅ LEGITIMATE (4 samples) - Real Communications
| File | Type | Example |
|------|------|---------|
| ham_legitimate.eml | Corporate | Meeting notes |
| legitimate_work.eml | HR | Performance review |
| legitimate_amazon.eml | Order | Shipment notification |
| legitimate_github.eml | Service | Security alert |

---

## 🧪 Recommended Testing Order

### Beginner (Easy Cases)
1. **spam_offer.eml** - Obviously spam
2. **ham_legitimate.eml** - Obviously legitimate
3. **phishing_bank.eml** - Obviously phishing

### Intermediate (More Challenges)
4. legitimate_amazon.eml
5. phishing_amazon.eml
6. spam_software.eml

### Advanced (Harder Detection)
7-13. All remaining files in any order

---

## 📈 After Testing Each File, Check:

✓ **Classification is correct**
- PHISHING for phishing files
- SPAM for spam files  
- LEGITIMATE for legitimate files

✓ **Confidence score is high** (90%+ for obvious cases)

✓ **Indicators/reasons** are clearly explained

✓ **Dashboard updates** with new statistics

✓ **History page** shows the analyzed email

✓ **Compliance report** records the classification

---

## 💾 File Details

### All Files Are:
- ✓ Safe to analyze (no malicious code)
- ✓ Real email format (RFC-compliant EML)
- ✓ Complete with headers and body
- ✓ Properly formatted for testing

### File Sizes:
- Average: 2-5 KB each
- All files < 10 KB
- No attachments
- No external dependencies

---

## 🔗 Related Resources

- **Main Guide**: `E:\projectpcr\EML_SAMPLES_GUIDE.md`
- **Sample README**: `E:\projectpcr\samples\README.md`
- **Dashboard**: http://localhost:5000
- **Analyzer**: http://localhost:5000/analyze

---

## 🎉 You're Ready!

Everything is set up. Just:
1. Download/copy the EML files
2. Use PhishGuard to analyze them
3. Watch the classifications work in real-time
4. Check statistics and history pages

**Enjoy testing your email security system! 🛡️**
