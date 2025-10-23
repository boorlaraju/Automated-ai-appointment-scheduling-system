"""
Simple Flask App for Team_Vet
Works without complex scheduling modules
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mock data for demonstration
doctors = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "General Practice", "experience_years": 8},
    {"id": 2, "name": "Dr. Michael Chen", "specialty": "Surgery", "experience_years": 12},
    {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Emergency", "experience_years": 6},
    {"id": 4, "name": "Dr. James Wilson", "specialty": "Dermatology", "experience_years": 10},
    {"id": 5, "name": "Dr. Lisa Thompson", "specialty": "Cardiology", "experience_years": 15}
]

appointments = []
booking_id_counter = 1

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         scheduling_available=True,
                         system_status=get_system_status())

@app.route('/test')
def test():
    """Simple test route"""
    return "<h1>Team_Vet Flask App is Working!</h1><p>Server is running successfully.</p>"

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_appointment():
    """Schedule a new appointment"""
    if request.method == 'GET':
        return render_template('schedule.html')
    
    try:
        patient_data = request.json
        result = schedule_mock_appointment(patient_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get scheduling recommendations"""
    try:
        patient_data = request.json
        recommendations = generate_mock_recommendations(patient_data)
        return jsonify({'success': True, 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/appointments')
def view_appointments():
    """View all appointments"""
    return render_template('appointments.html', appointments=appointments)

@app.route('/analytics')
def analytics():
    """View system analytics"""
    analytics_data = get_mock_analytics()
    return render_template('analytics.html', analytics=analytics_data)

@app.route('/doctors')
def view_doctors():
    """View available doctors"""
    return render_template('doctors.html', doctors=doctors)

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(get_system_status())

@app.route('/chatbot')
def chatbot():
    """Chatbot interface"""
    return render_template('chatbot.html')

@app.route('/inventory')
def inventory():
    """Inventory management interface"""
    inventory_data = get_mock_inventory()
    return render_template('inventory.html', inventory=inventory_data)

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    """API endpoint for chatbot messages"""
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        
        # Generate mock chatbot response
        response = generate_mock_chatbot_response(user_message)
        return jsonify(response)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/inventory', methods=['GET', 'POST'])
def api_inventory():
    """API endpoint for inventory management"""
    try:
        if request.method == 'GET':
            inventory_data = get_mock_inventory()
            return jsonify({'success': True, 'inventory': inventory_data})
        else:
            # Handle inventory updates
            data = request.json
            action = data.get('action', '')
            
            if action == 'add_medicine':
                result = add_mock_medicine(data)
            elif action == 'update_stock':
                result = update_mock_stock(data)
            else:
                result = {'success': False, 'message': 'Invalid action'}
            
            return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

def get_system_status():
    """Get current system status"""
    return {
        'scheduling_available': True,
        'scheduler_initialized': True,
        'data_path_exists': True,
        'models_trained': True,
        'total_appointments': len(appointments),
        'available_slots': 25
    }

def schedule_mock_appointment(patient_data):
    """Mock appointment scheduling"""
    global booking_id_counter
    
    # Select a random doctor
    doctor = random.choice(doctors)
    
    # Generate appointment time (next 7 days)
    days_ahead = random.randint(1, 7)
    appointment_time = datetime.now() + timedelta(days=days_ahead)
    appointment_time = appointment_time.replace(hour=random.randint(9, 17), minute=0, second=0)
    
    # Create booking
    booking = {
        'booking_id': booking_id_counter,
        'patient_name': patient_data.get('patient_name', 'Unknown'),
        'pet_name': patient_data.get('pet_name', 'Unknown'),
        'pet_type': patient_data.get('pet_type', 'Dog'),
        'appointment_type': patient_data.get('appointment_type', 'Checkup'),
        'urgency': patient_data.get('urgency', 'Medium'),
        'notes': patient_data.get('notes', ''),
        'booked_at': datetime.now().isoformat(),
        'status': 'confirmed'
    }
    
    # Create slot
    slot = {
        'slot_id': booking_id_counter,
        'doctor_id': doctor['id'],
        'doctor_name': doctor['name'],
        'specialty': doctor['specialty'],
        'datetime': appointment_time.isoformat(),
        'duration_minutes': int(patient_data.get('duration_minutes', 30)),
        'is_available': False
    }
    
    # Add to appointments
    appointments.append({
        'booking': booking,
        'slot': slot,
        'start_time': appointment_time,
        'end_time': appointment_time + timedelta(minutes=slot['duration_minutes'])
    })
    
    booking_id_counter += 1
    
    return {
        'success': True,
        'booking': booking,
        'slot': slot,
        'ml_predictions': {
            'success_probability': random.uniform(0.85, 0.95),
            'predicted_duration': slot['duration_minutes'],
            'recommendation_score': random.uniform(0.8, 0.95)
        }
    }

def generate_mock_recommendations(patient_data):
    """Generate mock recommendations"""
    recommendations = []
    
    for i in range(3):
        doctor = random.choice(doctors)
        days_ahead = random.randint(1, 7)
        appointment_time = datetime.now() + timedelta(days=days_ahead)
        appointment_time = appointment_time.replace(hour=random.randint(9, 17), minute=0, second=0)
        
        recommendations.append({
            'doctor_name': doctor['name'],
            'specialty': doctor['specialty'],
            'datetime': appointment_time.isoformat(),
            'success_probability': random.uniform(0.8, 0.95),
            'predicted_duration': random.randint(30, 60),
            'recommendation_score': random.uniform(0.8, 0.95)
        })
    
    return recommendations

def get_mock_analytics():
    """Get mock analytics data"""
    return {
        'total_appointments': len(appointments),
        'success_rate': 0.942,
        'appointment_type_distribution': {
            'Checkup': 45,
            'Vaccination': 25,
            'Surgery': 15,
            'Emergency': 10,
            'Follow-up': 5
        },
        'urgency_distribution': {
            'Low': 30,
            'Medium': 50,
            'High': 15,
            'Emergency': 5
        },
        'average_duration_minutes': 42.5,
        'feature_importance': {
            'doctor_experience': 0.25,
            'specialty_match': 0.20,
            'urgency_score': 0.15,
            'day_of_week': 0.10,
            'hour_of_day': 0.10,
            'pet_type_encoded': 0.10,
            'appointment_type_encoded': 0.10
        }
    }

def generate_mock_chatbot_response(user_message):
    """Generate mock chatbot response"""
    responses = {
        'hello': "Hello! I'm your AI veterinary assistant. How can I help you today?",
        'appointment': "I can help you schedule an appointment. What type of pet do you have?",
        'emergency': "For emergencies, please call our emergency line at (555) 123-4567 or visit our clinic immediately.",
        'vaccination': "Vaccinations are important for your pet's health. What type of pet do you have?",
        'surgery': "Our surgical team is highly experienced. What type of procedure does your pet need?",
        'cost': "Pricing varies by service. I can help you get an estimate - what service do you need?",
        'hours': "Our clinic is open Monday-Friday 8AM-6PM, Saturday 9AM-4PM, and Sunday 10AM-3PM.",
        'location': "We're located at 123 Veterinary Street, Pet City, PC 12345."
    }
    
    # Simple keyword matching
    user_lower = user_message.lower()
    for keyword, response in responses.items():
        if keyword in user_lower:
            return {
                'success': True,
                'message': response,
                'suggestions': [
                    "Schedule an appointment",
                    "Emergency contact",
                    "Vaccination info",
                    "Surgery information"
                ]
            }
    
    # Default response
    return {
        'success': True,
        'message': "I understand you're looking for help. Could you please provide more details about what you need assistance with?",
        'suggestions': [
            "Schedule an appointment",
            "Emergency contact",
            "General information",
            "Speak to a human"
        ]
    }

def get_mock_inventory():
    """Get mock inventory data"""
    return {
        'medicines': [
            {
                'id': 1,
                'name': 'Amoxicillin 250mg',
                'category': 'Antibiotic',
                'stock_quantity': 150,
                'unit': 'tablets',
                'expiry_date': '2024-12-31',
                'supplier': 'VetPharma Inc',
                'cost_per_unit': 2.50,
                'status': 'In Stock'
            },
            {
                'id': 2,
                'name': 'Rabies Vaccine',
                'category': 'Vaccine',
                'stock_quantity': 45,
                'unit': 'vials',
                'expiry_date': '2024-08-15',
                'supplier': 'VetVax Corp',
                'cost_per_unit': 15.00,
                'status': 'In Stock'
            },
            {
                'id': 3,
                'name': 'Pain Relief Syrup',
                'category': 'Pain Management',
                'stock_quantity': 8,
                'unit': 'bottles',
                'expiry_date': '2024-06-30',
                'supplier': 'PetCare Solutions',
                'cost_per_unit': 25.00,
                'status': 'Low Stock'
            },
            {
                'id': 4,
                'name': 'Surgical Gloves',
                'category': 'Supplies',
                'stock_quantity': 500,
                'unit': 'pairs',
                'expiry_date': '2025-12-31',
                'supplier': 'MedSupply Co',
                'cost_per_unit': 0.50,
                'status': 'In Stock'
            }
        ],
        'low_stock_items': 1,
        'expiring_soon': 2,
        'total_value': 1250.00
    }

def add_mock_medicine(data):
    """Add mock medicine to inventory"""
    return {
        'success': True,
        'message': 'Medicine added successfully',
        'medicine_id': len(get_mock_inventory()['medicines']) + 1
    }

def update_mock_stock(data):
    """Update mock stock quantity"""
    return {
        'success': True,
        'message': 'Stock updated successfully'
    }

if __name__ == '__main__':
    print("=" * 60)
    print("TEAM_VET - SIMPLE VETERINARY MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Starting web server...")
    print("The interface will open automatically in your browser.")
    print("If it doesn't open, go to: http://127.0.0.1:5000")
    print("=" * 60)
    
    # Run Flask app
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
