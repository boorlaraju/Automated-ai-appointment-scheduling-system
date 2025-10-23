"""
Automatic Scheduler for Veterinary Appointments
Main orchestrator that combines ML predictions with availability management
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json
import os
from .ml_model import SchedulingMLModel
from .availability_manager import AvailabilityManager
from .data_generator import DummyDataGenerator

class AutoScheduler:
    def __init__(self, data_path: str = "vet/scheduling/data/"):
        self.data_path = data_path
        self.ml_model = SchedulingMLModel()
        self.availability_manager = AvailabilityManager(data_path)
        self.data_generator = DummyDataGenerator()
        
        # Ensure data directory exists
        os.makedirs(data_path, exist_ok=True)
        os.makedirs(os.path.join(data_path, "models"), exist_ok=True)
    
    def initialize_system(self, generate_new_data: bool = True):
        """Initialize the scheduling system with data and models"""
        print("Initializing Veterinary Scheduling System...")
        
        # Generate dummy data if needed
        if generate_new_data or not os.path.exists(os.path.join(self.data_path, "appointments_dataset.csv")):
            print("Generating training data...")
            self.data_generator.generate_training_dataset()
            self.data_generator.save_doctors_data()
        
        # Load and train ML models
        if os.path.exists(os.path.join(self.data_path, "appointments_dataset.csv")):
            print("Loading training data...")
            df = pd.read_csv(os.path.join(self.data_path, "appointments_dataset.csv"))
            
            print("Training ML models...")
            model_metrics = self.ml_model.train_models(df)
            print(f"Model training completed with metrics: {model_metrics}")
        else:
            print("No training data found. Please generate data first.")
            return False
        
        # Initialize availability slots if not exists
        if not os.path.exists(os.path.join(self.data_path, "availability_slots.json")):
            print("Initializing availability slots...")
            self._initialize_availability_slots()
        
        print("System initialization completed!")
        return True
    
    def _initialize_availability_slots(self):
        """Initialize availability slots for all doctors"""
        # Load doctors data
        with open(os.path.join(self.data_path, "doctors.json"), 'r') as f:
            doctors = json.load(f)
        
        # Generate availability for next 30 days
        base_time = datetime.now()
        
        for doctor in doctors:
            for day in range(30):
                current_date = base_time + timedelta(days=day)
                
                # Skip weekends for some doctors
                if current_date.weekday() >= 5 and np.random.random() < 0.3:
                    continue
                
                # Generate 4-8 slots per day
                num_slots = np.random.randint(4, 9)
                start_hour = 9
                
                for slot in range(num_slots):
                    slot_time = current_date.replace(
                        hour=start_hour + slot,
                        minute=0,
                        second=0,
                        microsecond=0
                    )
                    
                    self.availability_manager.add_availability_slot(
                        doctor_id=doctor['id'],
                        start_time=slot_time,
                        duration_minutes=30,
                        slot_type="regular"
                    )
        
        print(f"Generated availability slots for {len(doctors)} doctors")
    
    def schedule_appointment(self, patient_info: Dict, preferences: Optional[Dict] = None) -> Dict:
        """Automatically schedule an appointment using ML recommendations"""
        print(f"Scheduling appointment for {patient_info.get('patient_name', 'Unknown')}")
        
        # Get available slots
        available_slots = self.availability_manager.get_available_slots()
        
        if not available_slots:
            return {
                'success': False,
                'message': 'No available slots found',
                'recommendations': []
            }
        
        # Get ML-based recommendations
        recommendations = self.ml_model.generate_scheduling_recommendations(
            patient_info, available_slots
        )
        
        # Apply preferences if provided
        if preferences:
            recommendations = self._apply_preferences(recommendations, preferences)
        
        # Select best recommendation
        if recommendations:
            best_slot = recommendations[0]
            
            try:
                # Book the appointment
                booking = self.availability_manager.book_appointment(
                    best_slot['slot_id'], patient_info
                )
                
                return {
                    'success': True,
                    'booking': booking,
                    'slot': best_slot,
                    'ml_predictions': {
                        'success_probability': best_slot['success_probability'],
                        'predicted_duration': best_slot['predicted_duration'],
                        'recommendation_score': best_slot['recommendation_score']
                    },
                    'alternatives': recommendations[1:5]  # Top 4 alternatives
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Booking failed: {str(e)}',
                    'recommendations': recommendations[:5]
                }
        else:
            return {
                'success': False,
                'message': 'No suitable slots found',
                'recommendations': []
            }
    
    def _apply_preferences(self, recommendations: List[Dict], preferences: Dict) -> List[Dict]:
        """Apply user preferences to recommendations"""
        filtered_recommendations = []
        
        for rec in recommendations:
            # Filter by doctor preference
            if 'preferred_doctor_id' in preferences:
                if rec['doctor_id'] != preferences['preferred_doctor_id']:
                    continue
            
            # Filter by time preference
            if 'preferred_time_range' in preferences:
                slot_time = datetime.fromisoformat(rec['datetime'])
                start_hour, end_hour = preferences['preferred_time_range']
                if not (start_hour <= slot_time.hour <= end_hour):
                    continue
            
            # Filter by date preference
            if 'preferred_dates' in preferences:
                slot_date = datetime.fromisoformat(rec['datetime']).date()
                if slot_date not in preferences['preferred_dates']:
                    continue
            
            # Apply preference bonus to score
            rec['recommendation_score'] += preferences.get('preference_bonus', 0.0)
            filtered_recommendations.append(rec)
        
        # Re-sort by updated scores
        filtered_recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return filtered_recommendations
    
    def get_schedule_recommendations(self, patient_info: Dict, 
                                   num_recommendations: int = 5) -> List[Dict]:
        """Get scheduling recommendations without booking"""
        available_slots = self.availability_manager.get_available_slots()
        
        if not available_slots:
            return []
        
        recommendations = self.ml_model.generate_scheduling_recommendations(
            patient_info, available_slots
        )
        
        return recommendations[:num_recommendations]
    
    def reschedule_appointment(self, booking_id: int, new_preferences: Optional[Dict] = None) -> Dict:
        """Reschedule an existing appointment"""
        # Get current booking
        current_booking = next(
            (b for b in self.availability_manager.bookings if b['booking_id'] == booking_id), 
            None
        )
        
        if not current_booking:
            return {'success': False, 'message': 'Booking not found'}
        
        # Get patient info from current booking
        patient_info = {
            'patient_name': current_booking['patient_name'],
            'pet_name': current_booking['pet_name'],
            'pet_type': current_booking['pet_type'],
            'appointment_type': current_booking['appointment_type'],
            'urgency': current_booking['urgency']
        }
        
        # Get new recommendations
        recommendations = self.get_schedule_recommendations(patient_info, 10)
        
        if not recommendations:
            return {'success': False, 'message': 'No alternative slots available'}
        
        # Apply new preferences
        if new_preferences:
            recommendations = self._apply_preferences(recommendations, new_preferences)
        
        # Try to reschedule to the best option
        if recommendations:
            try:
                new_booking = self.availability_manager.reschedule_appointment(
                    booking_id, recommendations[0]['slot_id']
                )
                
                return {
                    'success': True,
                    'new_booking': new_booking,
                    'alternatives': recommendations[1:5]
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Rescheduling failed: {str(e)}',
                    'alternatives': recommendations[:5]
                }
        
        return {'success': False, 'message': 'No suitable alternatives found'}
    
    def get_doctor_availability(self, doctor_id: int, days_ahead: int = 7) -> Dict:
        """Get doctor's availability summary"""
        return self.availability_manager.get_availability_summary(doctor_id, days_ahead)
    
    def get_system_analytics(self) -> Dict:
        """Get system analytics and performance metrics"""
        # Load appointment data
        if os.path.exists(os.path.join(self.data_path, "appointments_dataset.csv")):
            df = pd.read_csv(os.path.join(self.data_path, "appointments_dataset.csv"))
            
            # Calculate analytics
            total_appointments = len(df)
            successful_appointments = df['was_successful'].sum()
            success_rate = successful_appointments / total_appointments if total_appointments > 0 else 0
            
            # Appointment type distribution
            appointment_types = df['appointment_type'].value_counts().to_dict()
            
            # Urgency distribution
            urgency_dist = df['urgency'].value_counts().to_dict()
            
            # Average duration
            avg_duration = df['duration_minutes'].mean()
            
            return {
                'total_appointments': total_appointments,
                'success_rate': success_rate,
                'appointment_type_distribution': appointment_types,
                'urgency_distribution': urgency_dist,
                'average_duration_minutes': avg_duration,
                'feature_importance': self.ml_model.get_feature_importance()
            }
        else:
            return {'message': 'No data available for analytics'}
    
    def run_automatic_scheduling(self, patient_queue: List[Dict]) -> List[Dict]:
        """Run automatic scheduling for a queue of patients"""
        results = []
        
        print(f"Processing {len(patient_queue)} patients for automatic scheduling...")
        
        for i, patient in enumerate(patient_queue):
            print(f"Processing patient {i+1}/{len(patient_queue)}: {patient.get('patient_name', 'Unknown')}")
            
            result = self.schedule_appointment(patient)
            results.append({
                'patient': patient,
                'result': result
            })
            
            # Add small delay to simulate processing
            import time
            time.sleep(0.1)
        
        # Save results
        with open(os.path.join(self.data_path, "scheduling_results.json"), 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Automatic scheduling completed. Results saved to {self.data_path}scheduling_results.json")
        return results

if __name__ == "__main__":
    # Initialize and run the scheduler
    scheduler = AutoScheduler()
    
    # Initialize the system
    if scheduler.initialize_system():
        print("Scheduling system ready!")
        
        # Example usage
        patient_info = {
            'patient_name': 'John Doe',
            'pet_name': 'Buddy',
            'pet_type': 'Dog',
            'appointment_type': 'Checkup',
            'urgency': 'Medium',
            'notes': 'Regular checkup'
        }
        
        result = scheduler.schedule_appointment(patient_info)
        print(f"Scheduling result: {result}")
    else:
        print("Failed to initialize scheduling system")
