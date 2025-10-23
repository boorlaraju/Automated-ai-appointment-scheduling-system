"""
ML Model for Intelligent Veterinary Scheduling
Predicts optimal appointment scheduling based on historical data
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import joblib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class SchedulingMLModel:
    def __init__(self):
        self.success_classifier = None
        self.duration_predictor = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'doctor_experience', 'specialty_match', 'urgency_score',
            'day_of_week', 'hour_of_day', 'month', 'is_weekend',
            'pet_type_encoded', 'appointment_type_encoded'
        ]
        self.model_path = "vet/scheduling/models/"
        
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare data for training"""
        # Handle missing values
        df = df.fillna(0)
        
        # Prepare features
        X = df[self.feature_columns].values
        
        # Prepare targets
        y_success = df['was_successful'].astype(int).values
        y_duration = df['duration_minutes'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y_success, y_duration
    
    def train_models(self, df: pd.DataFrame) -> Dict[str, float]:
        """Train both success prediction and duration prediction models"""
        print("Preparing data for training...")
        X, y_success, y_duration = self.prepare_data(df)
        
        # Split data
        X_train, X_test, y_success_train, y_success_test = train_test_split(
            X, y_success, test_size=0.2, random_state=42, stratify=y_success
        )
        _, _, y_duration_train, y_duration_test = train_test_split(
            X, y_duration, test_size=0.2, random_state=42
        )
        
        print("Training success prediction model...")
        # Train success classifier
        self.success_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.success_classifier.fit(X_train, y_success_train)
        
        # Train duration predictor
        print("Training duration prediction model...")
        self.duration_predictor = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.duration_predictor.fit(X_train, y_duration_train)
        
        # Evaluate models
        success_pred = self.success_classifier.predict(X_test)
        duration_pred = self.duration_predictor.predict(X_test)
        
        success_accuracy = accuracy_score(y_success_test, success_pred)
        duration_mse = mean_squared_error(y_duration_test, duration_pred)
        
        print(f"Success prediction accuracy: {success_accuracy:.3f}")
        print(f"Duration prediction MSE: {duration_mse:.3f}")
        
        # Cross-validation scores
        success_cv = cross_val_score(self.success_classifier, X, y_success, cv=5)
        duration_cv = cross_val_score(self.duration_predictor, X, y_duration, cv=5)
        
        print(f"Success model CV score: {success_cv.mean():.3f} (+/- {success_cv.std() * 2:.3f})")
        print(f"Duration model CV score: {duration_cv.mean():.3f} (+/- {duration_cv.std() * 2:.3f})")
        
        # Save models
        self.save_models()
        
        return {
            'success_accuracy': success_accuracy,
            'duration_mse': duration_mse,
            'success_cv_mean': success_cv.mean(),
            'duration_cv_mean': duration_cv.mean()
        }
    
    def predict_appointment_success(self, features: Dict[str, Any]) -> float:
        """Predict probability of appointment success"""
        if self.success_classifier is None:
            raise ValueError("Model not trained. Call train_models() first.")
        
        # Convert features to array
        feature_array = np.array([[
            features.get('doctor_experience', 0),
            features.get('specialty_match', 0.5),
            features.get('urgency_score', 0.5),
            features.get('day_of_week', 0),
            features.get('hour_of_day', 12),
            features.get('month', 6),
            features.get('is_weekend', 0),
            features.get('pet_type_encoded', 0),
            features.get('appointment_type_encoded', 0)
        ]])
        
        # Scale features
        feature_array_scaled = self.scaler.transform(feature_array)
        
        # Predict probability
        success_prob = self.success_classifier.predict_proba(feature_array_scaled)[0][1]
        return success_prob
    
    def predict_appointment_duration(self, features: Dict[str, Any]) -> float:
        """Predict appointment duration in minutes"""
        if self.duration_predictor is None:
            raise ValueError("Model not trained. Call train_models() first.")
        
        # Convert features to array
        feature_array = np.array([[
            features.get('doctor_experience', 0),
            features.get('specialty_match', 0.5),
            features.get('urgency_score', 0.5),
            features.get('day_of_week', 0),
            features.get('hour_of_day', 12),
            features.get('month', 6),
            features.get('is_weekend', 0),
            features.get('pet_type_encoded', 0),
            features.get('appointment_type_encoded', 0)
        ]])
        
        # Scale features
        feature_array_scaled = self.scaler.transform(feature_array)
        
        # Predict duration
        duration = self.duration_predictor.predict(feature_array_scaled)[0]
        return max(15, min(120, duration))  # Clamp between 15-120 minutes
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the success classifier"""
        if self.success_classifier is None:
            return {}
        
        importance = self.success_classifier.feature_importances_
        return dict(zip(self.feature_columns, importance))
    
    def save_models(self):
        """Save trained models"""
        import os
        os.makedirs(self.model_path, exist_ok=True)
        
        if self.success_classifier:
            joblib.dump(self.success_classifier, f"{self.model_path}success_classifier.pkl")
        if self.duration_predictor:
            joblib.dump(self.duration_predictor, f"{self.model_path}duration_predictor.pkl")
        if self.scaler:
            joblib.dump(self.scaler, f"{self.model_path}scaler.pkl")
        
        print(f"Models saved to {self.model_path}")
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            self.success_classifier = joblib.load(f"{self.model_path}success_classifier.pkl")
            self.duration_predictor = joblib.load(f"{self.model_path}duration_predictor.pkl")
            self.scaler = joblib.load(f"{self.model_path}scaler.pkl")
            print("Models loaded successfully")
            return True
        except FileNotFoundError:
            print("Models not found. Train models first.")
            return False
    
    def generate_scheduling_recommendations(self, patient_info: Dict, available_slots: List[Dict]) -> List[Dict]:
        """Generate ML-based scheduling recommendations"""
        if not self.load_models():
            return available_slots
        
        recommendations = []
        
        for slot in available_slots:
            # Extract features for this slot
            slot_datetime = datetime.fromisoformat(slot['datetime'])
            
            features = {
                'doctor_experience': slot.get('doctor_experience', 5),
                'specialty_match': self._calculate_specialty_match(
                    slot.get('specialty', ''), patient_info.get('appointment_type', 'Checkup')
                ),
                'urgency_score': self._get_urgency_score(patient_info.get('urgency', 'Medium')),
                'day_of_week': slot_datetime.weekday(),
                'hour_of_day': slot_datetime.hour,
                'month': slot_datetime.month,
                'is_weekend': slot_datetime.weekday() >= 5,
                'pet_type_encoded': hash(patient_info.get('pet_type', 'Dog')) % 10,
                'appointment_type_encoded': hash(patient_info.get('appointment_type', 'Checkup')) % 10
            }
            
            # Get predictions
            success_prob = self.predict_appointment_success(features)
            predicted_duration = self.predict_appointment_duration(features)
            
            # Calculate recommendation score
            recommendation_score = self._calculate_recommendation_score(
                success_prob, predicted_duration, slot, patient_info
            )
            
            recommendations.append({
                **slot,
                'success_probability': success_prob,
                'predicted_duration': predicted_duration,
                'recommendation_score': recommendation_score,
                'ml_features': features
            })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return recommendations
    
    def _calculate_specialty_match(self, doctor_specialty: str, appointment_type: str) -> float:
        """Calculate specialty match score"""
        matches = {
            ("Surgery", "Surgery"): 1.0,
            ("Emergency", "Emergency"): 1.0,
            ("General Practice", "Checkup"): 0.9,
            ("General Practice", "Vaccination"): 0.8,
            ("Dermatology", "Checkup"): 0.7,
            ("Cardiology", "Checkup"): 0.6
        }
        return matches.get((doctor_specialty, appointment_type), 0.5)
    
    def _get_urgency_score(self, urgency: str) -> float:
        """Convert urgency to numeric score"""
        urgency_scores = {"Low": 0.2, "Medium": 0.5, "High": 0.8, "Emergency": 1.0}
        return urgency_scores.get(urgency, 0.5)
    
    def _calculate_recommendation_score(self, success_prob: float, predicted_duration: float, 
                                      slot: Dict, patient_info: Dict) -> float:
        """Calculate overall recommendation score"""
        base_score = success_prob * 0.4
        
        # Time preference (morning appointments preferred)
        time_score = 0.3 if 9 <= slot.get('hour', 12) <= 11 else 0.1
        
        # Duration match
        requested_duration = patient_info.get('duration_minutes', 30)
        duration_match = 1.0 - abs(predicted_duration - requested_duration) / requested_duration
        duration_score = duration_match * 0.2
        
        # Urgency factor
        urgency = patient_info.get('urgency', 'Medium')
        urgency_score = 0.1 if urgency in ['High', 'Emergency'] else 0.05
        
        return base_score + time_score + duration_score + urgency_score

if __name__ == "__main__":
    # This will be called when training the model
    model = SchedulingMLModel()
    print("ML Model class initialized. Use train_models() method to train.")
