# PhishGuard Sample Emails - Testing Guide

Download and use these sample EML files to test the PhishGuard email analyzer. Each file demonstrates different types of emails.

## 📬 How to Use Sample Emails

1. Download the EML file to your computer
2. Open PhishGuard Dashboard (http://localhost:5000)
3. Go to **"Analyze Email"** page
4. Click **"Choose File"** and select the EML file
5. Click **"Analyze"**
6. View the classification result

---

## 🚨 PHISHING Emails

These emails attempt to steal credentials or personal information by impersonating legitimate services.

### 1. **phishing_bank.eml**
- **Simulates:** Bank of America account alert
- **Tactic:** Fake suspicious login alert, urgency ("IMMEDIATE ACTION REQUIRED")
- **Red Flags:** Suspicious domain, malicious link, login urgency
- **Expected Result:** ❌ PHISHING

### 2. **phishing_amazon.eml**
- **Simulates:** Amazon account security alert
- **Tactic:** Locked account, verification request
- **Red Flags:** Non-official domain, suspicious link, account lock threat
- **Expected Result:** ❌ PHISHING

### 3. **phishing_paypal.eml**
- **Simulates:** PayPal billing problem notification
- **Tactic:** Payment method failure, service suspension threat
- **Red Flags:** Urgent action required, fake domain, malicious link
- **Expected Result:** ❌ PHISHING

### 4. **phishing_paypal2.eml**
- **Simulates:** PayPal payment method update
- **Tactic:** Billing issue, credential theft
- **Red Flags:** Suspicious sender, login request link
- **Expected Result:** ❌ PHISHING

### 5. **phishing_microsoft.eml**
- **Simulates:** Microsoft/Office 365 security alert
- **Tactic:** Unusual sign-in location, account restriction
- **Red Flags:** Unauthorized access warning, verification link
- **Expected Result:** ❌ PHISHING

### 6. **phishing_spoofed.eml**
- **Simulates:** Spoofed corporate email
- **Tactic:** Domain spoofing and impersonation
- **Expected Result:** ❌ PHISHING

---

## ⚠️ SPAM Emails

These emails are unsolicited commercial or bulk messages, often with misleading claims.

### 1. **spam_offer.eml**
- **Type:** Lottery/Prize scam
- **Tactic:** You've won money/prize, click to claim
- **Red Flags:** EXCESSIVE CAPS, multiple exclamation marks, urgent deadline
- **Expected Result:** ⚠️ SPAM

### 2. **spam_software.eml**
- **Type:** Software discount scam
- **Tactic:** Unrealistic discounts on premium software
- **Red Flags:** Too good to be true prices, pressure ("expires in 24 hours")
- **Expected Result:** ⚠️ SPAM

---

## ✅ LEGITIMATE Emails

These emails are genuine communications from real services.

### 1. **ham_legitimate.eml**
- **Type:** Internal company memo
- **Sender:** john.doe@company.com
- **Content:** Q4 meeting notes
- **Features:** Valid SPF, DKIM signatures, professional tone
- **Expected Result:** ✅ LEGITIMATE

### 2. **legitimate_work.eml**
- **Type:** HR notification
- **Content:** Performance review scheduling
- **Features:** Official company domain, DKIM-SPF authenticated
- **Expected Result:** ✅ LEGITIMATE

### 3. **legitimate_amazon.eml**
- **Type:** Order shipment notification
- **Content:** Order #111-2234567-1234567 shipped
- **Features:** Official amazon.com domain, order tracking info, authenticated
- **Expected Result:** ✅ LEGITIMATE

### 4. **legitimate_github.eml**
- **Type:** Security alert from GitHub
- **Content:** New sign-in detected notification
- **Features:** Official GitHub domain, security-focused content, no urgent action links
- **Expected Result:** ✅ LEGITIMATE

---

## 📊 Classification Breakdown

| Category | Count | Files |
|----------|-------|-------|
| **Phishing** | 6 | phishing_*.eml |
| **Spam** | 2 | spam_*.eml |
| **Legitimate** | 4 | ham_legitimate.eml, legitimate_*.eml |
| **Total** | 12 | All sample files |

---

## 🎯 Testing Strategy

For comprehensive testing, analyze all samples in this order:

1. **Start with Obvious Cases** (Spam emails first)
   - spam_offer.eml (obvious spam)
   - spam_software.eml (unrealistic offer)

2. **Test Legitimate Emails**
   - legitimate_work.eml
   - legitimate_amazon.eml
   - ham_legitimate.eml

3. **Test Advanced Phishing** (harder to detect)
   - phishing_microsoft.eml (modern UI)
   - phishing_amazon.eml (mimics real brand)
   - phishing_bank.eml (classic banking phish)

4. **Test Variations**
   - phishing_paypal.eml vs phishing_paypal2.eml (different phishing tactics)

---

## 📝 What to Check

After analyzing each email, verify:

- ✓ **Correct Classification** (Phishing/Spam/Legitimate)
- ✓ **Confidence Score** (Should be high for obvious cases)
- ✓ **Indicators** (Shows reason for classification)
- ✓ **Analysis Time** (Should be < 1 second)
- ✓ **Statistics Update** (Dashboard should update with new analysis)

---

## 💡 Tips

- You can upload multiple emails and track patterns
- Check the Statistics page to see your test results
- Review the Compliance page for audit trail
- Use History page to review all analyzed emails
- All samples are safe to analyze (they're just text files)

---

**Enjoy testing PhishGuard! 🛡️**
