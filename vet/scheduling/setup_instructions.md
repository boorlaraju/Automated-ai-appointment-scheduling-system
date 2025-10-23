# Veterinary Scheduling System - Setup Instructions

## Quick Setup Guide

### 1. Install Python Dependencies

**Option A: Using pip (Recommended)**
```bash
pip install pandas numpy scikit-learn joblib python-dateutil
```

**Option B: Using requirements.txt**
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python -c "import pandas, numpy, sklearn; print('All dependencies installed successfully!')"
```

### 3. Run the Training Script
```bash
python train_model.py
```

This will:
- Generate dummy training data (1000 appointments)
- Train ML models for success prediction and duration estimation
- Test the complete scheduling system
- Save trained models and analytics

### 4. Test the System
```bash
python simple_test.py
```

## Troubleshooting

### If you get "ModuleNotFoundError":

1. **Check Python version**: Ensure you're using Python 3.8+
   ```bash
   python --version
   ```

2. **Install in user directory**:
   ```bash
   python -m pip install --user pandas numpy scikit-learn joblib
   ```

3. **Use virtual environment** (Recommended):
   ```bash
   python -m venv vet_env
   vet_env\Scripts\activate  # Windows
   pip install pandas numpy scikit-learn joblib
   ```

### If training fails:

1. **Check data directory**: Ensure `data/` folder exists
2. **Check permissions**: Ensure write access to the directory
3. **Run simple test first**: `python simple_test.py`

## Usage Examples

### Basic Usage
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

### Advanced Usage
```python
# Get recommendations without booking
recommendations = scheduler.get_schedule_recommendations(patient_info, 5)

# Reschedule an appointment
result = scheduler.reschedule_appointment(booking_id=1, new_preferences={
    'preferred_time_range': (9, 12)
})

# Get system analytics
analytics = scheduler.get_system_analytics()
```

## File Structure After Setup

```
vet/scheduling/
├── data/
│   ├── appointments_dataset.csv    # Training data
│   ├── availability_slots.csv     # Available time slots
│   ├── doctors.json               # Doctor information
│   ├── models/                    # Trained ML models
│   │   ├── success_classifier.pkl
│   │   ├── duration_predictor.pkl
│   │   └── scaler.pkl
│   └── training_report.json       # Training metrics
├── __init__.py
├── scheduler.py                   # Main scheduler
├── ml_model.py                    # ML models
├── availability_manager.py        # Availability management
├── data_generator.py             # Data generation
├── train_model.py                # Training script
├── simple_test.py                # Basic functionality test
└── README.md                     # Documentation
```

## Integration with Web Application

### Flask Example
```python
from flask import Flask, request, jsonify
from vet.scheduling import AutoScheduler

app = Flask(__name__)
scheduler = AutoScheduler()
scheduler.initialize_system()

@app.route('/schedule', methods=['POST'])
def schedule_appointment():
    patient_data = request.json
    result = scheduler.schedule_appointment(patient_data)
    return jsonify(result)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    patient_data = request.json
    recommendations = scheduler.get_schedule_recommendations(patient_data)
    return jsonify(recommendations)
```

### Django Example
```python
from django.http import JsonResponse
from vet.scheduling import AutoScheduler

scheduler = AutoScheduler()
scheduler.initialize_system()

def schedule_view(request):
    if request.method == 'POST':
        patient_data = request.POST
        result = scheduler.schedule_appointment(patient_data)
        return JsonResponse(result)
```

## Performance Metrics

The system provides several performance metrics:
- **Success Prediction Accuracy**: How well it predicts appointment success
- **Duration Prediction MSE**: How accurately it predicts appointment duration
- **Feature Importance**: Which factors most influence scheduling success
- **System Analytics**: Overall performance statistics

## Next Steps

1. **Customize the system** for your specific needs
2. **Integrate with your web application**
3. **Set up real-time data feeds**
4. **Configure production settings**
5. **Add additional ML models** for enhanced predictions

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `python simple_test.py` to verify basic functionality
3. Check the `data/training_report.json` for detailed metrics
4. Review the logs for specific error messages
