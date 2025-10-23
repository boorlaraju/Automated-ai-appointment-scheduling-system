# Veterinary Scheduling System

An intelligent automatic scheduling system for veterinary appointments with ML-powered recommendations.

## Features

- **Automatic Scheduling**: ML-based appointment scheduling with success prediction
- **Availability Management**: Real-time doctor availability and slot booking
- **Smart Recommendations**: AI-powered scheduling recommendations based on historical data
- **Conflict Resolution**: Automatic conflict detection and resolution
- **Analytics**: Comprehensive scheduling analytics and performance metrics

## Components

### 1. AutoScheduler (`scheduler.py`)
Main orchestrator that combines ML predictions with availability management.

### 2. ML Model (`ml_model.py`)
Machine learning models for:
- Appointment success prediction
- Duration prediction
- Feature importance analysis

### 3. Availability Manager (`availability_manager.py`)
Manages doctor availability, slot booking, and conflict resolution.

### 4. Data Generator (`data_generator.py`)
Generates realistic dummy datasets for training ML models.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Models
```bash
python train_model.py
```

This will:
- Generate dummy training data
- Train ML models
- Test the complete system
- Save models and analytics

### 3. Use the Scheduler
```python
from scheduler import AutoScheduler

# Initialize scheduler
scheduler = AutoScheduler()

# Initialize system (generates data and trains models)
scheduler.initialize_system()

# Schedule an appointment
patient_info = {
    'patient_name': 'John Doe',
    'pet_name': 'Buddy',
    'pet_type': 'Dog',
    'appointment_type': 'Checkup',
    'urgency': 'Medium'
}

result = scheduler.schedule_appointment(patient_info)
print(result)
```

## API Reference

### AutoScheduler

#### `schedule_appointment(patient_info, preferences=None)`
Automatically schedule an appointment using ML recommendations.

**Parameters:**
- `patient_info` (dict): Patient and appointment details
- `preferences` (dict, optional): Scheduling preferences

**Returns:**
- `dict`: Scheduling result with booking details and ML predictions

#### `get_schedule_recommendations(patient_info, num_recommendations=5)`
Get scheduling recommendations without booking.

#### `reschedule_appointment(booking_id, new_preferences=None)`
Reschedule an existing appointment.

#### `get_system_analytics()`
Get system performance analytics.

### ML Model Features

The ML model uses the following features for predictions:
- Doctor experience
- Specialty match score
- Urgency level
- Day of week
- Hour of day
- Month
- Weekend indicator
- Pet type
- Appointment type

## Data Structure

### Patient Information
```python
patient_info = {
    'patient_name': str,
    'pet_name': str,
    'pet_type': str,  # Dog, Cat, Bird, etc.
    'appointment_type': str,  # Checkup, Surgery, Emergency, etc.
    'urgency': str,  # Low, Medium, High, Emergency
    'notes': str
}
```

### Scheduling Preferences
```python
preferences = {
    'preferred_doctor_id': int,
    'preferred_time_range': (start_hour, end_hour),
    'preferred_dates': [date1, date2, ...],
    'preference_bonus': float
}
```

## File Structure

```
vet/scheduling/
├── __init__.py
├── scheduler.py              # Main scheduler
├── ml_model.py              # ML models
├── availability_manager.py  # Availability management
├── data_generator.py       # Data generation
├── train_model.py          # Training script
├── requirements.txt        # Dependencies
├── README.md              # Documentation
└── data/                  # Data directory
    ├── appointments_dataset.csv
    ├── availability_slots.csv
    ├── doctors.json
    ├── models/            # Trained models
    └── training_report.json
```

## Performance Metrics

The system tracks several performance metrics:
- Success prediction accuracy
- Duration prediction MSE
- Cross-validation scores
- Feature importance rankings
- System analytics

## Integration

To integrate with your web application:

1. **Initialize the scheduler** in your application startup
2. **Use the API** to schedule appointments
3. **Handle results** and display recommendations to users
4. **Update availability** as appointments are booked/cancelled

## Example Integration

```python
# In your web application
from vet.scheduling import AutoScheduler

# Initialize once at startup
scheduler = AutoScheduler()
scheduler.initialize_system()

# In your API endpoint
@app.route('/schedule', methods=['POST'])
def schedule_appointment():
    patient_data = request.json
    result = scheduler.schedule_appointment(patient_data)
    return jsonify(result)
```

## Future Enhancements

- Real-time data integration
- Advanced ML models (deep learning)
- Multi-clinic support
- Patient preference learning
- Automated rescheduling
- Integration with calendar systems
