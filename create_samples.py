"""
Sample Email Generator
Create test emails for demonstrating the system
"""

from pathlib import Path

def create_sample_emails():
    """Create sample email files for testing"""
    
    # Create directories
    Path("samples").mkdir(exist_ok=True)
    
    # Fix encoding for Windows
    import sys
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 1. Legitimate Email (HAM)
    ham_email = """From: john.doe@company.com
To: jane.smith@company.com
Subject: Q4 Meeting Notes
Date: Mon, 19 Jan 2024 10:00:00 +0000
Message-ID: <abc123@company.com>
DKIM-Signature: v=1; a=rsa-sha256; d=company.com; s=default
Received-SPF: pass
Content-Type: text/plain; charset=utf-8

Hi Jane,

Thank you for attending the Q4 planning meeting yesterday. Here are the key takeaways:

1. Revenue targets for Q4 2024
2. New product launch timeline
3. Team expansion plans

Please review the attached presentation and let me know if you have any questions.

Best regards,
John Doe
Senior Project Manager
Company Inc.
"""
    
    # 2. Spam Email
    spam_email = """From: deals@super-offers.xyz
To: user@example.com
Subject: 🎉 CONGRATULATIONS! You've Won $1,000,000!!!
Date: Mon, 19 Jan 2024 11:30:00 +0000
Message-ID: <spam456@super-offers.xyz>
Content-Type: text/html; charset=utf-8

<html>
<body>
<h1>🎊 YOU ARE A WINNER! 🎊</h1>

<p><b>CONGRATULATIONS!!!</b> You have been selected as our LUCKY winner!</p>

<p>Click here NOW to claim your prize: <a href="http://suspicious-site.tk/claim">CLAIM NOW!</a></p>

<p><font color="red"><b>ACT FAST! This offer expires in 24 hours!!!</b></font></p>

<p>Don't miss this INCREDIBLE opportunity!!!</p>

<p>Visit our site for MORE amazing deals: http://bit.ly/fake123</p>

</body>
</html>
"""
    
    # 3. Phishing Email
    phishing_email = """From: security@paypa1-secure.com
To: victim@example.com
Subject: URGENT: Your PayPal Account Has Been Limited
Date: Mon, 19 Jan 2024 12:45:00 +0000
Message-ID: <phish789@paypa1-secure.com>
Reply-To: phisher@malicious-server.com
Content-Type: text/html; charset=utf-8

<html>
<body style="font-family: Arial, sans-serif;">

<div style="background-color: #003087; padding: 20px;">
    <h2 style="color: white;">PayPal Account Review</h2>
</div>

<div style="padding: 20px;">
    <p><b>Dear Valued Customer,</b></p>
    
    <p>We have detected unusual activity on your PayPal account. For your security, 
    we have temporarily limited your account access.</p>
    
    <p><font color="red"><b>IMPORTANT: You must verify your identity within 24 hours 
    or your account will be permanently suspended.</b></font></p>
    
    <p>To restore full access, please click the link below:</p>
    
    <p><a href="http://192.168.1.100/paypal-verify.php" 
    style="background-color: #0070ba; color: white; padding: 10px 20px; text-decoration: none;">
    Verify Your Account Now</a></p>
    
    <p>If you do not verify within 24 hours, you will lose access to:</p>
    <ul>
        <li>Send and receive money</li>
        <li>Withdraw funds</li>
        <li>Access transaction history</li>
    </ul>
    
    <p>We apologize for any inconvenience.</p>
    
    <p>Sincerely,<br>
    PayPal Security Team</p>
    
    <p style="font-size: 10px; color: gray;">
    Reference ID: SEC-2024-892347<br>
    Case Number: PP-URG-7821
    </p>
</div>

</body>
</html>
"""
    
    # 4. Advanced Phishing (Banking)
    banking_phish = """From: alerts@bank0famerica-secure.com
To: customer@example.com
Subject: Suspicious Activity Detected on Your Account
Date: Mon, 19 Jan 2024 14:20:00 +0000
Message-ID: <bank321@bank0famerica-secure.com>
Return-Path: attacker@evil-server.ru
Content-Type: text/html; charset=utf-8

<html>
<body>

<img src="http://malicious.com/fake-logo.png" alt="Bank Logo">

<h3>Account Security Alert</h3>

<p>Dear Customer,</p>

<p>We have identified suspicious login attempts on your Bank of America account 
from the following locations:</p>

<ul>
    <li>Nigeria - January 19, 2024 at 2:15 AM</li>
    <li>Russia - January 19, 2024 at 3:30 AM</li>
</ul>

<p><b style="color: red;">IMMEDIATE ACTION REQUIRED</b></p>

<p>To protect your account, please verify your identity by clicking the secure link below:</p>

<p><a href="http://bank-verify-secure.tk/login.php">Secure Verification Portal</a></p>

<p>For your security, this link will expire in 2 hours.</p>

<p>If you did not attempt to access your account, please contact us immediately at 
the number on the back of your card.</p>

<p>Thank you for banking with us.</p>

<p>Bank of America Security Department<br>
Reference: SEC-BA-2024-1847</p>

</body>
</html>
"""
    
    # 5. Spoofed Domain Email
    spoofed_email = """From: support@g00gle-security.com
To: user@example.com
Subject: Google Account - Unusual Sign-in Activity
Date: Mon, 19 Jan 2024 15:00:00 +0000
Message-ID: <goog987@g00gle-security.com>
Content-Type: text/plain

Google Account Security Alert

Hello,

We noticed a new sign-in to your Google Account from a device you don't usually use.

Device: Windows PC
Location: Unknown
Time: Today at 3:00 PM

If this was you, you can ignore this email.

If this wasn't you, please secure your account immediately by clicking:
http://accounts-google-verify.com/security

This link expires in 1 hour.

Google Security Team
"""
    
    # Save sample emails
    samples = {
        "ham_legitimate.eml": ham_email,
        "spam_offer.eml": spam_email,
        "phishing_paypal.eml": phishing_email,
        "phishing_bank.eml": banking_phish,
        "phishing_spoofed.eml": spoofed_email
    }
    
    for filename, content in samples.items():
        filepath = Path("samples") / filename
        filepath.write_text(content, encoding='utf-8')
        print(f"Created: {filepath}")
    
    print(f"\n✓ Created {len(samples)} sample email files in 'samples/' directory")
    print("\nTest them with:")
    print("  python cli.py analyze samples/ham_legitimate.eml")
    print("  python cli.py analyze samples/phishing_paypal.eml")
    print("  python cli.py batch samples/")

if __name__ == "__main__":
    create_sample_emails()