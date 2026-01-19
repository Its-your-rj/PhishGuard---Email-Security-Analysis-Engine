"""
Email Parser Module
Parses email headers, content, and extracts features
"""

import email
import re
import hashlib
from email import policy
from email.parser import BytesParser
from typing import Dict, List, Any
from urllib.parse import urlparse
import socket
from datetime import datetime

class EmailParser:
    """Parse and analyze email files"""
    
    def __init__(self):
        self.suspicious_keywords = [
            'urgent', 'verify', 'suspended', 'locked', 'confirm',
            'click here', 'act now', 'limited time', 'expire',
            'password', 'account', 'security', 'billing', 'payment'
        ]
        
        self.phishing_patterns = [
            r'verify.*account',
            r'suspended.*account',
            r'confirm.*identity',
            r'update.*payment',
            r'click.*link.*below',
            r'reset.*password'
        ]
    
    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """Parse email file and extract all features"""
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        
        return self.parse_message(msg)
    
    def parse_message(self, msg) -> Dict[str, Any]:
        """Parse email message object"""
        
        parsed = {
            'headers': self._parse_headers(msg),
            'from': msg.get('from', ''),
            'to': msg.get('to', ''),
            'subject': msg.get('subject', ''),
            'date': msg.get('date', ''),
            'body': self._extract_body(msg),
            'urls': [],
            'attachments': [],
            'features': {}
        }
        
        # Extract URLs
        parsed['urls'] = self._extract_urls(parsed['body'])
        
        # Extract attachments info
        parsed['attachments'] = self._extract_attachments(msg)
        
        # Calculate features
        parsed['features'] = self._calculate_features(parsed, msg)
        
        return parsed
    
    def _parse_headers(self, msg) -> Dict[str, Any]:
        """Parse and analyze email headers (mxtoolbox/mailheader.org standards)"""
        headers = {}
        
        # Basic headers
        for key in msg.keys():
            headers[key] = msg.get(key, '')
        
        # Authentication headers (comprehensive)
        headers['spf'] = self._check_spf(msg)
        headers['dkim'] = self._check_dkim(msg)
        headers['dmarc'] = self._check_dmarc(msg)
        headers['arc'] = self._check_arc(msg)
        
        # Received headers (routing path)
        headers['received_chain'] = msg.get_all('received', [])
        headers['hop_count'] = len(headers['received_chain'])
        
        # Reply-To analysis
        from_addr = self._extract_email(msg.get('from', ''))
        reply_to = self._extract_email(msg.get('reply-to', ''))
        headers['reply_to_mismatch'] = (reply_to != '' and from_addr != reply_to)
        headers['has_reply_to'] = reply_to != ''
        
        # Return-Path analysis
        return_path = self._extract_email(msg.get('return-path', ''))
        headers['return_path_mismatch'] = (return_path != '' and from_addr != return_path)
        headers['has_return_path'] = return_path != ''
        
        # Sender field check
        sender = self._extract_email(msg.get('sender', ''))
        headers['has_sender'] = sender != ''
        
        # X-headers spam indicators
        headers['x_originating_ip'] = msg.get('X-Originating-IP', '')
        headers['x_mailer'] = msg.get('X-Mailer', '')
        headers['x_priority'] = msg.get('X-Priority', '')
        headers['importance'] = msg.get('Importance', '')
        headers['x_spam_score'] = msg.get('X-Spam-Score', '')
        headers['x_spam_flag'] = msg.get('X-Spam-Flag', '')
        headers['x_spam_status'] = msg.get('X-Spam-Status', '')
        
        # List headers
        headers['list_unsubscribe'] = msg.get('List-Unsubscribe', '')
        headers['list_id'] = msg.get('List-ID', '')
        headers['list_help'] = msg.get('List-Help', '')
        
        # Content-Type and encoding
        headers['content_type'] = msg.get('Content-Type', '')
        headers['mime_version'] = msg.get('MIME-Version', '')
        
        # Server info
        headers['received_from_servers'] = self._extract_received_servers(msg)
        
        return headers
    
    def _extract_body(self, msg) -> str:
        """Extract email body content"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
                elif content_type == 'text/html':
                    try:
                        html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        body += self._html_to_text(html_content)
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())
        
        return body
    
    def _html_to_text(self, html: str) -> str:
        """Simple HTML to text conversion"""
        # Remove script and style tags
        html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_urls(self, text: str) -> List[Dict[str, str]]:
        """Extract and analyze URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        analyzed_urls = []
        seen_urls = set()  # Avoid duplicates
        
        for url in urls:
            if url not in seen_urls:
                seen_urls.add(url)
                parsed = urlparse(url)
                analyzed_urls.append({
                    'url': url,
                    'domain': parsed.netloc,
                    'suspicious': self._is_suspicious_url(url, parsed.netloc),
                    'shortened': self._is_shortened_url(parsed.netloc),
                    'ip_based': self._is_ip_url(url)
                })
        
        return analyzed_urls
    
    def _is_ip_url(self, url: str) -> bool:
        """Check if URL uses IP address instead of domain"""
        pattern = r'http[s]?://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        return bool(re.search(pattern, url))
    
    def _is_suspicious_url(self, url: str, domain: str) -> bool:
        """Check if URL is suspicious (enhanced)"""
        url_lower = url.lower()
        domain_lower = domain.lower()
        
        suspicious_patterns = [
            # IP address instead of domain
            (r'http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', 'IP address URL'),
            # Localhost or private IP ranges
            (r'http[s]?://(localhost|127\.0\.0\.1|192\.168\.|10\.|172\.1[6-9]\.|172\.2[0-9]\.|172\.3[0-1]\.)', 'Private IP'),
            # Mixed numbers and letters (obfuscation)
            (r'[0-9]+[a-z]+[0-9]+', 'Obfuscated domain'),
            # Free/cheap domains
            (r'\.tk$|\.ml$|\.ga$|\.cf$|\.tk\?|\.ml\?|\.ga\?|\.cf\?', 'Free domain TLD'),
        ]
        
        for pattern, _ in suspicious_patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                return True
        
        # Check for domain spoofing patterns
        suspicious_brand_patterns = [
            (r'paypa[l1]', 'paypal'),
            (r'amaz[o0]n', 'amazon'),
            (r'app[l1]e', 'apple'),
            (r'micros[o0]ft', 'microsoft'),
            (r'g[o0]{2}gle', 'google'),
            (r'[l1]nked[i1]n', 'linkedin'),
            (r'fa[c]ebook', 'facebook'),
            (r'twitter', 'twitter'),
            (r'ba[n]k', 'bank'),
        ]
        
        for pattern, brand in suspicious_brand_patterns:
            if re.search(pattern, domain_lower):
                # Only flag if it's NOT the exact brand domain
                if brand not in domain_lower or len(domain_lower) > len(brand) + 4:
                    return True
        
        return False
    
    def _is_shortened_url(self, domain: str) -> bool:
        """Check if URL is from a shortening service"""
        shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd']
        return any(shortener in domain for shortener in shorteners)
    
    def _extract_attachments(self, msg) -> List[Dict[str, str]]:
        """Extract attachment information"""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        attachments.append({
                            'filename': filename,
                            'content_type': part.get_content_type(),
                            'size': len(part.get_payload(decode=True) or b''),
                            'suspicious': self._is_suspicious_attachment(filename)
                        })
        
        return attachments
    
    def _is_suspicious_attachment(self, filename: str) -> bool:
        """Check if attachment is suspicious"""
        suspicious_extensions = [
            '.exe', '.bat', '.cmd', '.scr', '.vbs', 
            '.js', '.jar', '.zip', '.rar', '.7z'
        ]
        return any(filename.lower().endswith(ext) for ext in suspicious_extensions)
    
    def _calculate_features(self, parsed: Dict, msg) -> Dict[str, Any]:
        """Calculate ML features from parsed email"""
        body = parsed['body'].lower()
        urls = parsed['urls']
        
        # Count URL types
        ip_based_urls = sum(1 for u in urls if u.get('ip_based', False))
        shortened_urls = sum(1 for u in urls if u.get('shortened', False))
        
        # Check for signature (common in professional emails)
        has_signature = any(phrase in body for phrase in [
            'regards,', 'sincerely,', 'best regards', 'thank you',
            'phone:', 'ext:', '---', '___', 'sent from'
        ])
        
        features = {
            # Content features
            'body_length': len(parsed['body']),
            'url_count': len(urls),
            'suspicious_url_count': sum(1 for u in urls if u['suspicious']),
            'ip_based_url_count': ip_based_urls,
            'shortened_url_count': shortened_urls,
            'attachment_count': len(parsed['attachments']),
            'suspicious_attachment_count': sum(1 for a in parsed['attachments'] if a['suspicious']),
            
            # Keyword features
            'urgent_keyword_count': sum(body.count(kw) for kw in self.suspicious_keywords),
            'phishing_pattern_matches': sum(1 for p in self.phishing_patterns if re.search(p, body, re.IGNORECASE)),
            
            # Header features
            'has_spf': parsed['headers'].get('spf', 'NONE') in ['PASS', 'PRESENT'],
            'has_dkim': parsed['headers'].get('dkim', 'NONE') in ['PASS', 'PRESENT'],
            'has_dmarc': parsed['headers'].get('dmarc', 'NONE') in ['PASS'],
            'reply_to_mismatch': parsed['headers'].get('reply_to_mismatch', False),
            'return_path_mismatch': parsed['headers'].get('return_path_mismatch', False),
            'has_return_path': parsed['headers'].get('has_return_path', False),
            'has_reply_to': parsed['headers'].get('has_reply_to', False),
            
            # Sender features
            'from_domain': self._extract_domain(parsed['from']),
            'from_matches_domain': self._check_domain_match(parsed['from'], parsed['headers']),
            
            # HTML features
            'has_html': '<html' in parsed['body'].lower(),
            'html_to_text_ratio': self._calculate_html_ratio(msg),
            
            # Special characters
            'exclamation_count': body.count('!'),
            'question_count': body.count('?'),
            'capital_ratio': sum(1 for c in parsed['body'] if c.isupper()) / max(len(parsed['body']), 1),
            
            # Professional indicators
            'has_signature': has_signature,
            'has_list_unsubscribe': len(parsed['headers'].get('list_unsubscribe', '')) > 0,
            'has_list_id': len(parsed['headers'].get('list_id', '')) > 0,
            
            # Hop analysis
            'hop_count': parsed['headers'].get('hop_count', 0),
        }
        
        return features
    
    def _check_spf(self, msg) -> str:
        """Check SPF authentication (RFC 7208)"""
        # Check Received-SPF header first (most reliable)
        received_spf = msg.get('Received-SPF', '')
        if received_spf:
            if 'pass' in received_spf.lower():
                return 'PASS'
            elif 'fail' in received_spf.lower():
                return 'FAIL'
            elif 'softfail' in received_spf.lower():
                return 'SOFTFAIL'
            elif 'neutral' in received_spf.lower():
                return 'NEUTRAL'
            elif 'permerror' in received_spf.lower():
                return 'PERMERROR'
            elif 'temperror' in received_spf.lower():
                return 'TEMPERROR'
        
        # Check Authentication-Results header
        auth_results = msg.get('Authentication-Results', '')
        if auth_results and 'spf=' in auth_results.lower():
            if 'spf=pass' in auth_results.lower():
                return 'PASS'
            elif 'spf=fail' in auth_results.lower():
                return 'FAIL'
            elif 'spf=softfail' in auth_results.lower():
                return 'SOFTFAIL'
            elif 'spf=neutral' in auth_results.lower():
                return 'NEUTRAL'
        
        return 'NONE'
    
    def _check_dkim(self, msg) -> str:
        """Check DKIM signature (RFC 6376)"""
        dkim_sig = msg.get('DKIM-Signature', '')
        if dkim_sig:
            return 'PRESENT'
        
        # Check Authentication-Results header
        auth_results = msg.get('Authentication-Results', '')
        if auth_results and 'dkim=' in auth_results.lower():
            if 'dkim=pass' in auth_results.lower():
                return 'PASS'
            elif 'dkim=fail' in auth_results.lower():
                return 'FAIL'
            elif 'dkim=neutral' in auth_results.lower():
                return 'NEUTRAL'
            elif 'dkim=none' in auth_results.lower():
                return 'NONE'
        
        return 'NONE'
    
    def _check_dmarc(self, msg) -> str:
        """Check DMARC policy (RFC 7489)"""
        auth_results = msg.get('Authentication-Results', '')
        if auth_results and 'dmarc=' in auth_results.lower():
            if 'dmarc=pass' in auth_results.lower():
                return 'PASS'
            elif 'dmarc=fail' in auth_results.lower():
                return 'FAIL'
            elif 'dmarc=neutral' in auth_results.lower():
                return 'NEUTRAL'
            elif 'dmarc=none' in auth_results.lower():
                return 'NONE'
        
        return 'NONE'
    
    def _check_arc(self, msg) -> str:
        """Check ARC authentication (RFC 8617)"""
        arc_auth = msg.get('ARC-Authentication-Results', '')
        arc_seal = msg.get('ARC-Seal', '')
        
        if arc_seal:
            if 'pass' in arc_seal.lower():
                return 'PASS'
            elif 'fail' in arc_seal.lower():
                return 'FAIL'
        
        return 'NONE'
    
    def _extract_received_servers(self, msg) -> List[str]:
        """Extract server hostnames from Received headers"""
        servers = []
        received_headers = msg.get_all('Received', [])
        
        for received in received_headers:
            # Extract "from" server
            match = re.search(r'from\s+([\w\.\-]+)\s', received, re.IGNORECASE)
            if match:
                servers.append(match.group(1))
            # Extract "by" server
            match = re.search(r'by\s+([\w\.\-]+)(?:\s|;)', received, re.IGNORECASE)
            if match:
                servers.append(match.group(1))
        
        return servers
    
    def _extract_email(self, address: str) -> str:
        """Extract email address from formatted string"""
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', address)
        return match.group(0) if match else ''
    
    def _extract_domain(self, address: str) -> str:
        """Extract domain from email address"""
        email_addr = self._extract_email(address)
        if '@' in email_addr:
            return email_addr.split('@')[1]
        return ''
    
    def _check_domain_match(self, from_addr: str, headers: Dict) -> bool:
        """Check if sender domain matches authenticated domain"""
        from_domain = self._extract_domain(from_addr)
        
        # Check against Return-Path
        return_path = headers.get('Return-Path', '')
        return_domain = self._extract_domain(return_path)
        
        return from_domain == return_domain
    
    def _calculate_html_ratio(self, msg) -> float:
        """Calculate ratio of HTML to text content"""
        html_length = 0
        text_length = 0
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        if content_type == 'text/html':
                            html_length += len(payload)
                        elif content_type == 'text/plain':
                            text_length += len(payload)
                except:
                    pass
        
        if text_length == 0:
            return 1.0 if html_length > 0 else 0.0
        
        return html_length / max(text_length, 1)