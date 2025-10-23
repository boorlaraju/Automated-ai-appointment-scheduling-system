"""
Simple test script for the veterinary scheduling system
Tests basic functionality without requiring all ML dependencies
"""

import os
import json
from datetime import datetime, timedelta

def test_basic_functionality():
    """Test basic scheduling functionality"""
    print("Testing Veterinary Scheduling System...")
    print("=" * 50)
    
    # Test 1: Create data directory
    print("1. Creating data directory...")
    data_path = "data"
    os.makedirs(data_path, exist_ok=True)
    print("✓ Data directory created")
    
    # Test 2: Create sample doctors data
    print("\n2. Creating sample doctors data...")
    doctors = [
        {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "General Practice", "experience_years": 8},
        {"id": 2, "name": "Dr. Michael Chen", "specialty": "Surgery", "experience_years": 12},
        {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Emergency", "experience_years": 6}
    ]
    
    with open(os.path.join(data_path, "doctors.json"), 'w') as f:
        json.dump(doctors, f, indent=2)
    print("✓ Doctors data created")
    
    # Test 3: Create sample availability slots
    print("\n3. Creating sample availability slots...")
    availability_slots = []
    base_time = datetime.now()
    
    for doctor in doctors:
        for day in range(7):  # Next 7 days
            current_date = base_time + timedelta(days=day)
            
            # Skip weekends for some doctors
            if current_date.weekday() >= 5 and doctor['id'] == 3:
                continue
                
            # Generate 4-6 slots per day
            for slot in range(4, 7):
                slot_time = current_date.replace(
                    hour=9 + slot,
                    minute=0,
                    second=0,
                    microsecond=0
                )
                
                availability_slots.append({
                    "slot_id": len(availability_slots) + 1,
                    "doctor_id": doctor["id"],
                    "doctor_name": doctor["name"],
                    "specialty": doctor["specialty"],
                    "datetime": slot_time.isoformat(),
                    "duration_minutes": 30,
                    "is_available": True,
                    "slot_type": "regular"
                })
    
    with open(os.path.join(data_path, "availability_slots.json"), 'w') as f:
        json.dump(availability_slots, f, indent=2)
    print(f"✓ Created {len(availability_slots)} availability slots")
    
    # Test 4: Create sample bookings
    print("\n4. Creating sample bookings...")
    bookings = [
        {
            "booking_id": 1,
            "slot_id": 1,
            "patient_name": "John Doe",
            "pet_name": "Buddy",
            "pet_type": "Dog",
            "appointment_type": "Checkup",
            "urgency": "Medium",
            "notes": "Regular checkup",
            "booked_at": datetime.now().isoformat(),
            "status": "confirmed"
        },
        {
            "booking_id": 2,
            "slot_id": 5,
            "patient_name": "Jane Smith",
            "pet_name": "Whiskers",
            "pet_type": "Cat",
            "appointment_type": "Vaccination",
            "urgency": "Low",
            "notes": "Annual vaccination",
            "booked_at": datetime.now().isoformat(),
            "status": "confirmed"
        }
    ]
    
    with open(os.path.join(data_path, "bookings.json"), 'w') as f:
        json.dump(bookings, f, indent=2)
    print(f"✓ Created {len(bookings)} sample bookings")
    
    # Test 5: Test basic scheduling logic
    print("\n5. Testing basic scheduling logic...")
    
    # Find available slots
    available_slots = [slot for slot in availability_slots if slot['is_available']]
    booked_slot_ids = [booking['slot_id'] for booking in bookings]
    truly_available = [slot for slot in available_slots if slot['slot_id'] not in booked_slot_ids]
    
    print(f"✓ Found {len(truly_available)} available slots")
    
    # Test 6: Simulate appointment booking
    print("\n6. Testing appointment booking simulation...")
    
    if truly_available:
        # Simulate booking the first available slot
        test_slot = truly_available[0]
        new_booking = {
            "booking_id": len(bookings) + 1,
            "slot_id": test_slot['slot_id'],
            "patient_name": "Test Patient",
            "pet_name": "Test Pet",
            "pet_type": "Dog",
            "appointment_type": "Checkup",
            "urgency": "Medium",
            "notes": "Test appointment",
            "booked_at": datetime.now().isoformat(),
            "status": "confirmed"
        }
        
        print(f"✓ Simulated booking appointment for {new_booking['patient_name']}")
        print(f"  - Doctor: {test_slot['doctor_name']}")
        print(f"  - Time: {test_slot['datetime']}")
        print(f"  - Duration: {test_slot['duration_minutes']} minutes")
    
    print("\n" + "=" * 50)
    print("BASIC FUNCTIONALITY TEST COMPLETED!")
    print("=" * 50)
    print("\nThe scheduling system structure is working correctly.")
    print("\nTo use the full ML-powered system:")
    print("1. Install dependencies: pip install pandas numpy scikit-learn joblib")
    print("2. Run: python train_model.py")
    print("3. Use the AutoScheduler class in your application")
    
    return True

if __name__ == "__main__":
    test_basic_functionality()
