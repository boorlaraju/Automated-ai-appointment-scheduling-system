"""
Dummy Data Generator for Veterinary Scheduling System
Generates realistic training data for ML model
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

class DummyDataGenerator:
    def __init__(self):
        self.doctors = [
            {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "General Practice", "experience_years": 8},
            {"id": 2, "name": "Dr. Michael Chen", "specialty": "Surgery", "experience_years": 12},
            {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Emergency", "experience_years": 6},
            {"id": 4, "name": "Dr. James Wilson", "specialty": "Dermatology", "experience_years": 10},
            {"id": 5, "name": "Dr. Lisa Thompson", "specialty": "Cardiology", "experience_years": 15}
        ]
        
        self.pet_types = ["Dog", "Cat", "Bird", "Rabbit", "Hamster", "Fish", "Reptile"]
        self.urgency_levels = ["Low", "Medium", "High", "Emergency"]
        self.appointment_types = ["Checkup", "Vaccination", "Surgery", "Emergency", "Follow-up", "Grooming"]
        
    def generate_availability_slots(self, days_ahead: int = 30) -> List[Dict]:
        """Generate availability slots for doctors"""
        slots = []
        base_time = datetime.now()
        
        for doctor in self.doctors:
            for day in range(days_ahead):
                current_date = base_time + timedelta(days=day)
                
                # Skip weekends for some doctors
                if current_date.weekday() >= 5 and random.random() < 0.3:
                    continue
                    
                # Generate 4-8 slots per day
                num_slots = random.randint(4, 8)
                start_hour = 9
                
                for slot in range(num_slots):
                    slot_time = current_date.replace(
                        hour=start_hour + slot,
                        minute=0,
                        second=0,
                        microsecond=0
                    )
                    
                    # Some slots are already booked
                    is_available = random.random() > 0.3
                    
                    slots.append({
                        "doctor_id": doctor["id"],
                        "doctor_name": doctor["name"],
                        "specialty": doctor["specialty"],
                        "datetime": slot_time.isoformat(),
                        "duration_minutes": 30,
                        "is_available": is_available,
                        "slot_type": "regular"
                    })
        
        return slots
    
    def generate_patient_appointments(self, num_appointments: int = 1000) -> List[Dict]:
        """Generate historical appointment data"""
        appointments = []
        
        for i in range(num_appointments):
            # Random date in the past 6 months
            days_ago = random.randint(1, 180)
            appointment_date = datetime.now() - timedelta(days=days_ago)
            
            doctor = random.choice(self.doctors)
            pet_type = random.choice(self.pet_types)
            urgency = random.choice(self.urgency_levels)
            appointment_type = random.choice(self.appointment_types)
            
            # Calculate success probability based on various factors
            success_prob = self._calculate_success_probability(
                doctor, pet_type, urgency, appointment_type, appointment_date
            )
            
            # Generate outcome
            was_successful = random.random() < success_prob
            
            # Generate features for ML
            features = {
                "doctor_experience": doctor["experience_years"],
                "specialty_match": self._get_specialty_match_score(doctor["specialty"], appointment_type),
                "urgency_score": self._get_urgency_score(urgency),
                "day_of_week": appointment_date.weekday(),
                "hour_of_day": appointment_date.hour,
                "month": appointment_date.month,
                "is_weekend": appointment_date.weekday() >= 5,
                "pet_type_encoded": hash(pet_type) % 10,
                "appointment_type_encoded": hash(appointment_type) % 10
            }
            
            appointments.append({
                "appointment_id": i + 1,
                "patient_name": f"Patient_{i+1}",
                "pet_name": f"Pet_{i+1}",
                "pet_type": pet_type,
                "doctor_id": doctor["id"],
                "doctor_name": doctor["name"],
                "specialty": doctor["specialty"],
                "appointment_type": appointment_type,
                "urgency": urgency,
                "scheduled_datetime": appointment_date.isoformat(),
                "duration_minutes": random.choice([30, 45, 60]),
                "was_successful": was_successful,
                "no_show": not was_successful and random.random() < 0.15,
                "rescheduled": not was_successful and random.random() < 0.1,
                "features": features
            })
        
        return appointments
    
    def _calculate_success_probability(self, doctor: Dict, pet_type: str, urgency: str, 
                                    appointment_type: str, appointment_date: datetime) -> float:
        """Calculate probability of successful appointment"""
        base_prob = 0.8
        
        # Doctor experience factor
        exp_factor = min(doctor["experience_years"] / 15, 1.0) * 0.1
        
        # Specialty match factor
        specialty_match = self._get_specialty_match_score(doctor["specialty"], appointment_type)
        specialty_factor = specialty_match * 0.15
        
        # Urgency factor
        urgency_factor = self._get_urgency_score(urgency) * 0.1
        
        # Time factors
        time_factor = 0.05 if appointment_date.hour in [9, 10, 14, 15] else -0.05
        weekend_factor = -0.1 if appointment_date.weekday() >= 5 else 0.05
        
        # Pet type factor
        pet_factor = 0.05 if pet_type in ["Dog", "Cat"] else -0.05
        
        success_prob = base_prob + exp_factor + specialty_factor + urgency_factor + time_factor + weekend_factor + pet_factor
        return max(0.1, min(0.95, success_prob))
    
    def _get_specialty_match_score(self, specialty: str, appointment_type: str) -> float:
        """Calculate how well doctor specialty matches appointment type"""
        matches = {
            ("Surgery", "Surgery"): 1.0,
            ("Emergency", "Emergency"): 1.0,
            ("General Practice", "Checkup"): 0.9,
            ("General Practice", "Vaccination"): 0.8,
            ("Dermatology", "Checkup"): 0.7,
            ("Cardiology", "Checkup"): 0.6
        }
        return matches.get((specialty, appointment_type), 0.5)
    
    def _get_urgency_score(self, urgency: str) -> float:
        """Convert urgency level to numeric score"""
        urgency_scores = {"Low": 0.2, "Medium": 0.5, "High": 0.8, "Emergency": 1.0}
        return urgency_scores.get(urgency, 0.5)
    
    def generate_training_dataset(self) -> pd.DataFrame:
        """Generate complete training dataset"""
        print("Generating availability slots...")
        availability_slots = self.generate_availability_slots()
        
        print("Generating appointment history...")
        appointments = self.generate_patient_appointments()
        
        # Convert to DataFrame
        df_appointments = pd.DataFrame(appointments)
        
        # Flatten features
        feature_columns = list(appointments[0]["features"].keys())
        for col in feature_columns:
            df_appointments[col] = df_appointments["features"].apply(lambda x: x[col])
        
        df_appointments = df_appointments.drop("features", axis=1)
        
        # Save datasets
        df_appointments.to_csv("vet/scheduling/data/appointments_dataset.csv", index=False)
        
        availability_df = pd.DataFrame(availability_slots)
        availability_df.to_csv("vet/scheduling/data/availability_slots.csv", index=False)
        
        print(f"Generated {len(appointments)} appointments and {len(availability_slots)} availability slots")
        print("Datasets saved to vet/scheduling/data/")
        
        return df_appointments
    
    def save_doctors_data(self):
        """Save doctors information"""
        with open("vet/scheduling/data/doctors.json", "w") as f:
            json.dump(self.doctors, f, indent=2)
        print("Doctors data saved to vet/scheduling/data/doctors.json")

if __name__ == "__main__":
    generator = DummyDataGenerator()
    dataset = generator.generate_training_dataset()
    generator.save_doctors_data()
    print("Dummy dataset generation completed!")
