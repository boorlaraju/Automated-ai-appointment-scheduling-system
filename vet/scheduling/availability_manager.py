"""
Availability Manager for Veterinary Scheduling
Manages doctor availability, slot booking, and conflict resolution
"""

from datetime import datetime, timedelta, time
from typing import List, Dict, Any, Optional
import json
import os

class AvailabilityManager:
    def __init__(self, data_path: str = "vet/scheduling/data/"):
        self.data_path = data_path
        self.availability_file = os.path.join(data_path, "availability_slots.json")
        self.bookings_file = os.path.join(data_path, "bookings.json")
        self.availability_slots = []
        self.bookings = []
        self.load_data()
    
    def load_data(self):
        """Load availability and booking data"""
        # Load availability slots
        if os.path.exists(self.availability_file):
            with open(self.availability_file, 'r') as f:
                self.availability_slots = json.load(f)
        else:
            self.availability_slots = []
        
        # Load bookings
        if os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'r') as f:
                self.bookings = json.load(f)
        else:
            self.bookings = []
    
    def save_data(self):
        """Save availability and booking data"""
        os.makedirs(self.data_path, exist_ok=True)
        
        with open(self.availability_file, 'w') as f:
            json.dump(self.availability_slots, f, indent=2)
        
        with open(self.bookings_file, 'w') as f:
            json.dump(self.bookings, f, indent=2)
    
    def add_availability_slot(self, doctor_id: int, start_time: datetime, 
                            duration_minutes: int = 30, slot_type: str = "regular") -> Dict:
        """Add a new availability slot for a doctor"""
        slot = {
            "slot_id": len(self.availability_slots) + 1,
            "doctor_id": doctor_id,
            "start_time": start_time.isoformat(),
            "duration_minutes": duration_minutes,
            "slot_type": slot_type,
            "is_available": True,
            "created_at": datetime.now().isoformat()
        }
        
        self.availability_slots.append(slot)
        self.save_data()
        return slot
    
    def get_available_slots(self, doctor_id: Optional[int] = None, 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Dict]:
        """Get available slots with optional filters"""
        available_slots = []
        
        for slot in self.availability_slots:
            # Filter by doctor
            if doctor_id and slot['doctor_id'] != doctor_id:
                continue
            
            # Filter by date range
            slot_time = datetime.fromisoformat(slot['start_time'])
            if start_date and slot_time < start_date:
                continue
            if end_date and slot_time > end_date:
                continue
            
            # Check if slot is available
            if slot['is_available']:
                # Check if slot is not booked
                is_booked = any(
                    booking['slot_id'] == slot['slot_id'] 
                    for booking in self.bookings
                )
                
                if not is_booked:
                    available_slots.append(slot)
        
        return available_slots
    
    def book_appointment(self, slot_id: int, patient_info: Dict) -> Dict:
        """Book an appointment for a specific slot"""
        # Find the slot
        slot = next((s for s in self.availability_slots if s['slot_id'] == slot_id), None)
        if not slot:
            raise ValueError(f"Slot {slot_id} not found")
        
        if not slot['is_available']:
            raise ValueError(f"Slot {slot_id} is not available")
        
        # Check if slot is already booked
        existing_booking = next(
            (b for b in self.bookings if b['slot_id'] == slot_id), None
        )
        if existing_booking:
            raise ValueError(f"Slot {slot_id} is already booked")
        
        # Create booking
        booking = {
            "booking_id": len(self.bookings) + 1,
            "slot_id": slot_id,
            "patient_name": patient_info.get('patient_name', ''),
            "pet_name": patient_info.get('pet_name', ''),
            "pet_type": patient_info.get('pet_type', ''),
            "appointment_type": patient_info.get('appointment_type', 'Checkup'),
            "urgency": patient_info.get('urgency', 'Medium'),
            "notes": patient_info.get('notes', ''),
            "booked_at": datetime.now().isoformat(),
            "status": "confirmed"
        }
        
        self.bookings.append(booking)
        self.save_data()
        
        return booking
    
    def cancel_appointment(self, booking_id: int) -> bool:
        """Cancel an appointment"""
        booking = next((b for b in self.bookings if b['booking_id'] == booking_id), None)
        if not booking:
            return False
        
        booking['status'] = 'cancelled'
        booking['cancelled_at'] = datetime.now().isoformat()
        
        # Make the slot available again
        slot = next((s for s in self.availability_slots if s['slot_id'] == booking['slot_id']), None)
        if slot:
            slot['is_available'] = True
        
        self.save_data()
        return True
    
    def reschedule_appointment(self, booking_id: int, new_slot_id: int) -> Dict:
        """Reschedule an appointment to a new slot"""
        booking = next((b for b in self.bookings if b['booking_id'] == booking_id), None)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")
        
        # Check if new slot is available
        new_slot = next((s for s in self.availability_slots if s['slot_id'] == new_slot_id), None)
        if not new_slot:
            raise ValueError(f"New slot {new_slot_id} not found")
        
        if not new_slot['is_available']:
            raise ValueError(f"New slot {new_slot_id} is not available")
        
        # Free up old slot
        old_slot = next((s for s in self.availability_slots if s['slot_id'] == booking['slot_id']), None)
        if old_slot:
            old_slot['is_available'] = True
        
        # Update booking
        booking['slot_id'] = new_slot_id
        booking['rescheduled_at'] = datetime.now().isoformat()
        booking['status'] = 'rescheduled'
        
        # Mark new slot as unavailable
        new_slot['is_available'] = False
        
        self.save_data()
        return booking
    
    def get_doctor_schedule(self, doctor_id: int, date: datetime) -> List[Dict]:
        """Get doctor's schedule for a specific date"""
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        schedule = []
        
        for booking in self.bookings:
            slot = next((s for s in self.availability_slots if s['slot_id'] == booking['slot_id']), None)
            if not slot or slot['doctor_id'] != doctor_id:
                continue
            
            slot_time = datetime.fromisoformat(slot['start_time'])
            if date_start <= slot_time <= date_end:
                schedule.append({
                    **booking,
                    'slot': slot,
                    'start_time': slot_time,
                    'end_time': slot_time + timedelta(minutes=slot['duration_minutes'])
                })
        
        # Sort by start time
        schedule.sort(key=lambda x: x['start_time'])
        return schedule
    
    def find_conflicts(self, doctor_id: int, start_time: datetime, duration_minutes: int) -> List[Dict]:
        """Find scheduling conflicts for a proposed appointment"""
        end_time = start_time + timedelta(minutes=duration_minutes)
        conflicts = []
        
        for booking in self.bookings:
            slot = next((s for s in self.availability_slots if s['slot_id'] == booking['slot_id']), None)
            if not slot or slot['doctor_id'] != doctor_id:
                continue
            
            slot_start = datetime.fromisoformat(slot['start_time'])
            slot_end = slot_start + timedelta(minutes=slot['duration_minutes'])
            
            # Check for time overlap
            if (start_time < slot_end and end_time > slot_start):
                conflicts.append({
                    'booking': booking,
                    'slot': slot,
                    'conflict_type': 'time_overlap',
                    'overlap_start': max(start_time, slot_start),
                    'overlap_end': min(end_time, slot_end)
                })
        
        return conflicts
    
    def get_availability_summary(self, doctor_id: int, days_ahead: int = 7) -> Dict:
        """Get availability summary for a doctor"""
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days_ahead)
        
        available_slots = self.get_available_slots(doctor_id, start_date, end_date)
        booked_slots = [b for b in self.bookings if b['status'] in ['confirmed', 'rescheduled']]
        
        # Count slots by day
        daily_summary = {}
        for slot in available_slots:
            slot_date = datetime.fromisoformat(slot['start_time']).date()
            if slot_date not in daily_summary:
                daily_summary[slot_date] = {'available': 0, 'booked': 0}
            daily_summary[slot_date]['available'] += 1
        
        # Count booked slots by day
        for booking in booked_slots:
            slot = next((s for s in self.availability_slots if s['slot_id'] == booking['slot_id']), None)
            if slot and slot['doctor_id'] == doctor_id:
                slot_date = datetime.fromisoformat(slot['start_time']).date()
                if start_date.date() <= slot_date <= end_date.date():
                    if slot_date not in daily_summary:
                        daily_summary[slot_date] = {'available': 0, 'booked': 0}
                    daily_summary[slot_date]['booked'] += 1
        
        return {
            'doctor_id': doctor_id,
            'period': f"{start_date.date()} to {end_date.date()}",
            'total_available_slots': len(available_slots),
            'total_booked_slots': len([b for b in booked_slots if b['status'] in ['confirmed', 'rescheduled']]),
            'daily_summary': daily_summary
        }
    
    def optimize_schedule(self, doctor_id: int, date: datetime) -> List[Dict]:
        """Optimize doctor's schedule for a specific date"""
        schedule = self.get_doctor_schedule(doctor_id, date)
        
        # Sort by start time
        schedule.sort(key=lambda x: x['start_time'])
        
        # Identify gaps and potential optimizations
        optimizations = []
        
        for i in range(len(schedule) - 1):
            current_end = schedule[i]['end_time']
            next_start = schedule[i + 1]['start_time']
            gap = next_start - current_end
            
            if gap.total_seconds() > 0:
                optimizations.append({
                    'type': 'gap',
                    'start_time': current_end,
                    'end_time': next_start,
                    'duration_minutes': gap.total_seconds() / 60,
                    'suggestion': f"Gap of {gap.total_seconds() / 60:.1f} minutes between appointments"
                })
        
        return optimizations

if __name__ == "__main__":
    # Initialize availability manager
    manager = AvailabilityManager()
    print("Availability Manager initialized")
