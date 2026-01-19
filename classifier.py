"""
Email Classifier Module
Classifies emails as HAM, SPAM, or PHISHING
"""

import re
import pickle
from typing import Dict, Any, List, Tuple
import numpy as np
from pathlib import Path

class EmailClassifier:
    """Classify emails using rule-based and ML approaches"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.vectorizer = None
        
        # Load trained model if available
        if model_path and Path(model_path).exists():
            self._load_model(model_path)
        
        # Rule-based thresholds
        self.phishing_threshold = 0.6
        self.spam_threshold = 0.5
        
        # Phishing indicators
        self.phishing_domains = [
            'paypal', 'amazon', 'apple', 'microsoft', 'google',
            'netflix', 'facebook', 'instagram', 'bank', 'verify'
        ]
        
        self.phishing_keywords = [
            'verify your account', 'suspended account', 'unusual activity',
            'confirm your identity', 'update payment', 'security alert',
            'click here immediately', 'account will be closed', 'reset password'
        ]
    
    def classify(self, parsed_email: Dict[str, Any]) -> Dict[str, Any]:
        """Classify email and return detailed results"""
        
        # Extract features
        features = parsed_email['features']
        
        # Rule-based classification
        rule_score, indicators = self._rule_based_classification(parsed_email, features)
        
        # ML-based classification (if model available)
        ml_score = 0.0
        if self.model:
            ml_score = self._ml_classification(parsed_email)
        
        # Combine scores
        final_score = (rule_score * 0.6) + (ml_score * 0.4) if self.model else rule_score
        
        # Determine classification
        classification, confidence = self._determine_class(final_score, indicators)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(classification, confidence)
        
        # Header analysis summary
        header_analysis = self._analyze_headers(parsed_email['headers'])
        
        return {
            'classification': classification,
            'confidence': confidence,
            'rule_score': rule_score,
            'ml_score': ml_score,
            'threat_indicators': indicators,
            'recommendation': recommendation,
            'header_analysis': header_analysis,
            'features': features
        }
    
    def _rule_based_classification(self, parsed: Dict, features: Dict) -> Tuple[float, List[str]]:
        """Rule-based classification using heuristics (industry standard)"""
        phishing_score = 0.0
        spam_score = 0.0
        indicators = []
        
        # =========================
        # CRITICAL PHISHING CHECKS
        # =========================
        
        # 1. Authentication failure - CRITICAL
        spf_status = parsed['headers'].get('spf', 'NONE')
        dkim_status = parsed['headers'].get('dkim', 'NONE')
        dmarc_status = parsed['headers'].get('dmarc', 'NONE')
        
        if spf_status in ['FAIL', 'SOFTFAIL']:
            phishing_score += 0.25
            indicators.append("⚠️  SPF authentication failed/softfail")
        elif spf_status == 'NONE':
            phishing_score += 0.15
            indicators.append("⚠️  No SPF authentication")
        
        if dkim_status == 'FAIL':
            phishing_score += 0.20
            indicators.append("⚠️  DKIM signature failed")
        elif dkim_status == 'NONE':
            phishing_score += 0.10
            indicators.append("⚠️  No DKIM signature")
        
        if dmarc_status == 'FAIL':
            phishing_score += 0.25
            indicators.append("⚠️  DMARC policy violated")
        elif dmarc_status == 'NONE':
            phishing_score += 0.10
            indicators.append("⚠️  No DMARC policy")
        
        # 2. Sender header mismatches - CRITICAL PHISHING
        if features.get('reply_to_mismatch'):
            phishing_score += 0.30
            indicators.append("🚨 Reply-To doesn't match sender (PHISHING)")
        
        if features.get('return_path_mismatch'):
            phishing_score += 0.20
            indicators.append("🚨 Return-Path doesn't match sender (PHISHING)")
        
        # 3. Suspicious/spoofed domain - CRITICAL
        from_domain = features.get('from_domain', '')
        if self._is_spoofed_domain(from_domain):
            phishing_score += 0.40
            indicators.append(f"🚨 Domain spoofing detected: {from_domain}")
        
        # 4. Suspicious URLs in body - HIGH PHISHING INDICATOR
        suspicious_url_count = features.get('suspicious_url_count', 0)
        if suspicious_url_count > 0:
            phishing_score += 0.35
            indicators.append(f"🚨 Contains {suspicious_url_count} suspicious URL(s) - PHISHING")
        
        if features.get('ip_based_url_count', 0) > 0:
            phishing_score += 0.30
            indicators.append(f"🚨 IP-based URLs detected - HIGH PHISHING RISK")
        
        if features.get('shortened_url_count', 0) > 2:
            phishing_score += 0.20
            indicators.append(f"⚠️  Multiple shortened URLs (obfuscation)")
        
        # 5. Phishing-specific keywords and patterns - HIGH INDICATOR
        phishing_matches = features.get('phishing_pattern_matches', 0)
        if phishing_matches > 0:
            phishing_score += 0.35
            indicators.append(f"🚨 Contains {phishing_matches} phishing pattern(s)")
        
        # 6. Urgent/Time pressure - PHISHING TACTIC
        urgent_count = features.get('urgent_keyword_count', 0)
        if urgent_count > 5:
            phishing_score += 0.25
            indicators.append(f"⚠️  High urgency language ({urgent_count} keywords)")
        elif urgent_count > 2:
            phishing_score += 0.10
            indicators.append(f"⚠️  Some urgency keywords detected")
        
        # 7. Suspicious attachments - PHISHING/MALWARE
        if features.get('suspicious_attachment_count', 0) > 0:
            phishing_score += 0.40
            indicators.append(f"🚨 Suspicious attachment(s) detected - HIGH RISK")
        
        # 8. HTML obfuscation - PHISHING TECHNIQUE
        html_ratio = features.get('html_to_text_ratio', 0)
        if html_ratio > 3.0:
            phishing_score += 0.20
            indicators.append("⚠️  HTML obfuscation detected (>3:1 ratio)")
        
        # =========================
        # SPAM-SPECIFIC CHECKS
        # =========================
        
        # 1. Excessive URLs - SPAM indicator
        url_count = features.get('url_count', 0)
        if url_count > 10:
            spam_score += 0.30
            indicators.append(f"📧 Excessive URLs ({url_count}) - SPAM")
        elif url_count > 5:
            spam_score += 0.15
            indicators.append(f"📧 Multiple URLs ({url_count})")
        
        # 2. Excessive exclamation marks - SPAM
        exclamation_count = features.get('exclamation_count', 0)
        if exclamation_count > 10:
            spam_score += 0.25
            indicators.append(f"📧 Excessive exclamation marks ({exclamation_count})")
        elif exclamation_count > 5:
            spam_score += 0.12
            indicators.append(f"📧 Multiple exclamation marks ({exclamation_count})")
        
        # 3. Missing professional headers - SPAM
        if not parsed['headers'].get('list_unsubscribe'):
            spam_score += 0.10
            # Only penalize if it looks commercial
            if any(kw in parsed['subject'].lower() for kw in ['offer', 'deal', 'sale', 'discount', 'buy']):
                indicators.append("📧 Missing List-Unsubscribe header (commercial email)")
        
        # 4. High capital ratio - SPAM
        capital_ratio = features.get('capital_ratio', 0)
        if capital_ratio > 0.3:
            spam_score += 0.15
            indicators.append("📧 Excessive CAPS (spam tactic)")
        
        # 5. Body length anomalies
        body_length = features.get('body_length', 0)
        if body_length < 50:
            spam_score += 0.10
            indicators.append("📧 Very short email (common spam)")
        elif body_length > 10000:
            spam_score += 0.08
            indicators.append("📧 Unusually long email")
        
        # =========================
        # NEGATIVE INDICATORS (REDUCES MALICIOUS SCORE)
        # =========================
        
        # Professional email signatures
        if features.get('has_signature', False):
            phishing_score *= 0.8
            spam_score *= 0.9
        
        # Valid SPF/DKIM/DMARC
        if spf_status == 'PASS':
            phishing_score *= 0.5
        
        if dkim_status == 'PASS':
            phishing_score *= 0.6
        
        if dmarc_status == 'PASS':
            phishing_score *= 0.5
        
        # Professional domain
        if self._is_professional_domain(from_domain):
            phishing_score *= 0.7
            spam_score *= 0.8
        
        # Determine which score is higher
        if phishing_score > spam_score:
            final_score = min(phishing_score, 1.0)
            score_type = "PHISHING"
        else:
            final_score = min(spam_score, 1.0)
            score_type = "SPAM"
        
        # If both are low, it's HAM
        if phishing_score < 0.3 and spam_score < 0.3:
            final_score = 0.0
            score_type = "HAM"
        
        return final_score, indicators
    
    def _is_spoofed_domain(self, domain: str) -> bool:
        """Check if domain appears to be spoofed"""
        if not domain:
            return False
        
        domain_lower = domain.lower()
        
        # Check for common brand names with typos
        for brand in self.phishing_domains:
            # Check for character substitution (e.g., paypa1 instead of paypal)
            if brand in domain_lower:
                # Check for numeric substitution (0->O, 1->L, 5->S)
                if re.search(r'[01l5]', domain_lower) and brand in ['paypal', 'amazon', 'apple', 'microsoft', 'google']:
                    # Verify it's actually different (not exact match)
                    brand_domain = f"{brand}.com"
                    if domain_lower != brand_domain and domain_lower != f"{brand}.co.uk":
                        return True
                # Check for hyphenated versions
                if '-' in domain_lower and brand in domain_lower:
                    brand_domain = f"{brand}.com"
                    if domain_lower != brand_domain:
                        return True
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'verify.*account',
            r'secure.*bank',
            r'confirm.*identity',
            r'update.*account',
            r'login.*secure',
            r'-support$',
            r'^support-',
            r'customer-care',
            r'account-verify',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, domain_lower):
                return True
        
        return False
    
    def _is_professional_domain(self, domain: str) -> bool:
        """Check if domain appears to be professional/legitimate"""
        if not domain:
            return False
        
        domain_lower = domain.lower()
        
        # Known legitimate domains
        professional_domains = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
            'apple.com', 'microsoft.com', 'google.com', 'amazon.com',
            'paypal.com', 'facebook.com', 'twitter.com', 'linkedin.com',
            'github.com', 'stackoverflow.com', 'reddit.com',
        ]
        
        if domain_lower in professional_domains:
            return True
        
        # Check if it has established corporate pattern
        # Has proper TLD (not free)
        legitimate_tlds = ['.com', '.org', '.gov', '.edu', '.net', '.co.uk', '.de', '.fr', '.au']
        if any(domain_lower.endswith(tld) for tld in legitimate_tlds):
            # And doesn't have suspicious patterns
            if not any(pattern in domain_lower for pattern in ['-', 'verify', 'secure', 'update', 'login', 'confirm']):
                return True
        
        return False
    
    def _ml_classification(self, parsed: Dict) -> float:
        """ML-based classification (placeholder for trained model)"""
        if not self.model or not self.vectorizer:
            return 0.0
        
        try:
            # Extract text features
            text = f"{parsed['subject']} {parsed['body']}"
            
            # Vectorize
            text_features = self.vectorizer.transform([text])
            
            # Predict probability
            proba = self.model.predict_proba(text_features)[0]
            
            # Return probability of being malicious (spam or phishing)
            return max(proba[1], proba[2]) if len(proba) > 2 else proba[1]
            
        except Exception as e:
            print(f"ML classification error: {e}")
            return 0.0
    
    def _determine_class(self, score: float, indicators: List[str]) -> Tuple[str, float]:
        """Determine final classification based on score and indicators"""
        
        # Count critical indicators
        phishing_indicators = sum(1 for ind in indicators if '🚨' in ind)
        spam_indicators = sum(1 for ind in indicators if '📧' in ind)
        warning_indicators = sum(1 for ind in indicators if '⚠️' in ind)
        
        # If we have multiple critical phishing indicators, it's phishing
        if phishing_indicators >= 2:
            return 'PHISHING', min(score + phishing_indicators * 0.15, 1.0)
        
        # If we have at least one critical indicator AND high score
        if phishing_indicators >= 1 and score >= 0.4:
            return 'PHISHING', min(score, 1.0)
        
        # Domain spoofing is almost always phishing
        if any('spoofing' in ind.lower() for ind in indicators):
            return 'PHISHING', min(score + 0.25, 1.0)
        
        # Suspicious attachments or IP-based URLs = phishing/malware
        if any('suspicious attachment' in ind.lower() or 'ip-based' in ind.lower() for ind in indicators):
            return 'PHISHING', min(score + 0.20, 1.0)
        
        # Multiple auth failures + header mismatches = phishing
        auth_fails = sum(1 for ind in indicators if any(x in ind.lower() for x in ['spf', 'dkim', 'dmarc']))
        header_mismatches = sum(1 for ind in indicators if any(x in ind.lower() for x in ["doesn't match", 'mismatch']))
        
        if auth_fails >= 2 and header_mismatches >= 1:
            return 'PHISHING', min(score + 0.10, 1.0)
        
        # If score is high and we have spam indicators, it's spam
        if score >= 0.35 and spam_indicators > 0:
            return 'SPAM', min(score, 1.0)
        
        # If we have phishing-related indicators
        if warning_indicators >= 3 and score >= 0.35:
            return 'PHISHING', min(score, 1.0)
        
        # If score is moderate with warnings
        if warning_indicators >= 2 and score >= 0.20:
            return 'SPAM', min(score, 1.0)
        
        # Low risk is HAM
        if score < 0.20:
            return 'HAM', 1.0 - score
        
        # Default: If moderate score, check what type
        if score >= 0.20:
            if any(ind for ind in indicators if 'phishing' in ind.lower() or 'spoofing' in ind.lower() or 'ip-based' in ind.lower()):
                return 'PHISHING', score
            else:
                return 'SPAM', score
        
        return 'HAM', 1.0 - score
    
    def _generate_recommendation(self, classification: str, confidence: float) -> str:
        """Generate action recommendation"""
        if classification == 'PHISHING':
            if confidence > 0.8:
                return "DELETE IMMEDIATELY - High confidence phishing attempt"
            else:
                return "QUARANTINE - Possible phishing attempt, verify before opening"
        elif classification == 'SPAM':
            if confidence > 0.7:
                return "MOVE TO SPAM - Likely spam email"
            else:
                return "REVIEW - Possible spam, check before acting"
        else:
            if confidence > 0.8:
                return "SAFE - Email appears legitimate"
            else:
                return "CAUTION - Exercise normal email security practices"
    
    def _analyze_headers(self, headers: Dict) -> Dict[str, str]:
        """Summarize header analysis"""
        analysis = {}
        
        # SPF
        spf = headers.get('spf', 'NONE')
        analysis['SPF'] = spf
        
        # DKIM
        dkim = headers.get('dkim', 'NONE')
        analysis['DKIM'] = dkim
        
        # DMARC
        dmarc = headers.get('dmarc', 'NONE')
        analysis['DMARC'] = dmarc
        
        # Hop count
        hop_count = headers.get('hop_count', 0)
        analysis['Hop Count'] = str(hop_count)
        if hop_count > 10:
            analysis['Hop Count Status'] = 'Suspicious (too many hops)'
        
        # Reply-To mismatch
        if headers.get('reply_to_mismatch'):
            analysis['Reply-To'] = 'Mismatch detected'
        
        # Return-Path mismatch
        if headers.get('return_path_mismatch'):
            analysis['Return-Path'] = 'Mismatch detected'
        
        return analysis
    
    def _load_model(self, model_path: str):
        """Load trained ML model"""
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.vectorizer = data['vectorizer']
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.vectorizer = None