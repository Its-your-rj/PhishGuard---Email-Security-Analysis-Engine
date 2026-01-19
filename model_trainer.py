"""
Model Trainer Module
Train ML models for spam/phishing detection
"""

import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from email_parser import EmailParser

class ModelTrainer:
    """Train and evaluate email classification models"""
    
    def __init__(self):
        self.parser = EmailParser()
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2
        )
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=30,
            random_state=42,
            n_jobs=-1
        )
    
    def train(self, dataset_dir: str, model_output: str, epochs: int = 10) -> Dict[str, float]:
        """Train model on dataset"""
        
        print("Loading dataset...")
        X_text, X_features, y, labels = self._load_dataset(dataset_dir)
        
        print(f"Dataset loaded: {len(y)} samples")
        print(f"Classes: {set(labels)}")
        
        # Split data
        X_text_train, X_text_test, X_feat_train, X_feat_test, y_train, y_test = train_test_split(
            X_text, X_features, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("\nTraining model...")
        
        # Fit vectorizer on training text
        X_text_train_vec = self.vectorizer.fit_transform(X_text_train)
        X_text_test_vec = self.vectorizer.transform(X_text_test)
        
        # Combine text features with numerical features
        X_train_combined = self._combine_features(X_text_train_vec, X_feat_train)
        X_test_combined = self._combine_features(X_text_test_vec, X_feat_test)
        
        # Train model
        self.model.fit(X_train_combined, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_combined)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted')
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)
        
        # Feature importance
        self._print_feature_importance()
        
        # Save model
        self._save_model(model_output)
        
        return metrics
    
    def _load_dataset(self, dataset_dir: str) -> Tuple[List[str], np.ndarray, List[int], List[str]]:
        """Load and parse dataset"""
        dataset_path = Path(dataset_dir)
        
        X_text = []
        X_features = []
        y = []
        labels = []
        
        # Expected structure: dataset_dir/ham/, dataset_dir/spam/, dataset_dir/phishing/
        label_map = {'ham': 0, 'spam': 1, 'phishing': 2}
        
        for label_name, label_id in label_map.items():
            label_dir = dataset_path / label_name
            
            if not label_dir.exists():
                print(f"Warning: {label_dir} not found")
                continue
            
            email_files = list(label_dir.glob('*.eml')) + list(label_dir.glob('*.txt'))
            
            for email_file in email_files:
                try:
                    parsed = self.parser.parse_file(str(email_file))
                    
                    # Text features
                    text = f"{parsed['subject']} {parsed['body']}"
                    X_text.append(text)
                    
                    # Numerical features
                    features = self._extract_numerical_features(parsed)
                    X_features.append(features)
                    
                    # Label
                    y.append(label_id)
                    labels.append(label_name)
                    
                except Exception as e:
                    print(f"Error parsing {email_file}: {e}")
        
        return X_text, np.array(X_features), y, labels
    
    def _extract_numerical_features(self, parsed: Dict) -> List[float]:
        """Extract numerical features for ML"""
        features = parsed['features']
        
        return [
            float(features.get('body_length', 0)),
            float(features.get('url_count', 0)),
            float(features.get('suspicious_url_count', 0)),
            float(features.get('attachment_count', 0)),
            float(features.get('suspicious_attachment_count', 0)),
            float(features.get('urgent_keyword_count', 0)),
            float(features.get('phishing_pattern_matches', 0)),
            float(features.get('has_spf', False)),
            float(features.get('has_dkim', False)),
            float(features.get('reply_to_mismatch', False)),
            float(features.get('return_path_mismatch', False)),
            float(features.get('html_to_text_ratio', 0)),
            float(features.get('exclamation_count', 0)),
            float(features.get('question_count', 0)),
            float(features.get('capital_ratio', 0)),
        ]
    
    def _combine_features(self, text_features, numerical_features):
        """Combine text and numerical features"""
        from scipy.sparse import hstack, csr_matrix
        
        # Convert numerical features to sparse matrix
        numerical_sparse = csr_matrix(numerical_features)
        
        # Combine
        combined = hstack([text_features, numerical_sparse])
        
        return combined
    
    def _print_feature_importance(self):
        """Print top feature importances"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            
            # Get top 10 features
            top_indices = np.argsort(importances)[-10:][::-1]
            
            print("\nTop 10 Important Features:")
            feature_names = self.vectorizer.get_feature_names_out().tolist()
            feature_names.extend([
                'body_length', 'url_count', 'suspicious_url_count',
                'attachment_count', 'suspicious_attachment_count',
                'urgent_keyword_count', 'phishing_pattern_matches',
                'has_spf', 'has_dkim', 'reply_to_mismatch',
                'return_path_mismatch', 'html_to_text_ratio',
                'exclamation_count', 'question_count', 'capital_ratio'
            ])
            
            for idx in top_indices:
                if idx < len(feature_names):
                    print(f"  {feature_names[idx]}: {importances[idx]:.4f}")
    
    def _save_model(self, output_path: str):
        """Save trained model and vectorizer"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'vectorizer': self.vectorizer
            }, f)
        
        print(f"\nModel saved to {output_path}")