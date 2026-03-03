import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from pathlib import Path

class EnhancedMLModel:
    """Enhanced ML model for PhishGuard with ensemble method"""
    
    def __init__(self, model_path="models/enhanced_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data['model']
                    self.vectorizer = data['vectorizer']
                    self.is_trained = True
                    print(f"Loaded model from {self.model_path}")
            except:
                self._create_new_model()
        else:
            self._create_new_model()
    
    def _create_new_model(self):
        """Create new ML model"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        self.is_trained = False
        print("Created new ML model")
    
    def train(self, emails_data, labels):
        """Train the ML model
        
        Args:
            emails_data: List of email texts
            labels: List of labels (0=HAM, 1=SPAM, 2=PHISHING)
        """
        if not emails_data or not labels:
            print("No training data provided")
            return False
        
        try:
            # Vectorize emails
            X = self.vectorizer.fit_transform(emails_data)
            y = np.array(labels)
            
            # Train model
            self.model.fit(X, y)
            self.is_trained = True
            
            # Save model
            self._save_model()
            print(f"Model trained with {len(emails_data)} samples")
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict(self, email_text):
        """Predict email classification
        
        Returns:
            (classification, confidence) tuple
            classification: 0=HAM, 1=SPAM, 2=PHISHING
            confidence: probability score 0-1
        """
        if not self.is_trained:
            return None, 0
        
        try:
            X = self.vectorizer.transform([email_text])
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            confidence = max(probabilities)
            
            return prediction, confidence
        except Exception as e:
            print(f"Error predicting: {e}")
            return None, 0
    
    def ensemble_predict(self, email_text, rule_based_score):
        """Combine rule-based and ML predictions
        
        Args:
            email_text: Email content
            rule_based_score: Score from rule-based classifier (0-1)
        
        Returns:
            Combined confidence score
        """
        if not self.is_trained:
            return rule_based_score
        
        try:
            ml_pred, ml_confidence = self.predict(email_text)
            
            # Ensemble: 60% rule-based, 40% ML
            combined_score = (rule_based_score * 0.6) + (ml_confidence * 0.4)
            return combined_score
        except:
            return rule_based_score
    
    def _save_model(self):
        """Save model to disk"""
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'vectorizer': self.vectorizer
            }, f)
        
        print(f"Model saved to {self.model_path}")
    
    def get_feature_importance(self):
        """Get feature importance from model"""
        if not self.is_trained or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importance = self.model.feature_importances_
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get top 10 features
        top_indices = np.argsort(importance)[-10:][::-1]
        top_features = {
            feature_names[i]: float(importance[i])
            for i in top_indices
        }
        
        return top_features
    
    def fine_tune(self, new_emails, new_labels):
        """Fine-tune model with new data"""
        if not self.is_trained:
            return self.train(new_emails, new_labels)
        
        try:
            # Get existing training data (approximate)
            X_new = self.vectorizer.transform(new_emails)
            y_new = np.array(new_labels)
            
            # Re-train with new data
            # Note: This is a simplified approach
            self.model.fit(X_new, y_new)
            self._save_model()
            
            print(f"Model fine-tuned with {len(new_emails)} new samples")
            return True
        except Exception as e:
            print(f"Error fine-tuning: {e}")
            return False
