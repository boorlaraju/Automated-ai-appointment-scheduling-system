"""
Flask Web Interface for Veterinary Scheduling System
Fixed version with proper imports
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import sys
from datetime import datetime, timedelta
import webbrowser
import threading
import time

# Add the scheduling module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
scheduling_dir = os.path.join(parent_dir, 'scheduling')
sys.path.insert(0, scheduling_dir)

# Try to import scheduling modules
SCHEDULING_AVAILABLE = False
scheduler = None

try:
    from scheduler import AutoScheduler
    from data_generator import DummyDataGenerator
    from availability_manager import AvailabilityManager
    SCHEDULING_AVAILABLE = True
    print("Scheduling modules loaded successfully")
except ImportError as e:
    print(f"Scheduling modules not available: {e}")
    SCHEDULING_AVAILABLE = False

app = Flask(__name__)

# Global scheduler instance
data_path = os.path.join(parent_dir, 'scheduling', 'data')

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         scheduling_available=SCHEDULING_AVAILABLE,
                         system_status=get_system_status())

@app.route('/initialize')
def initialize_system():
    """Initialize the scheduling system"""
    global scheduler
    
    if not SCHEDULING_AVAILABLE:
        return jsonify({'success': False, 'message': 'Scheduling modules not available'})
    
    try:
        scheduler = AutoScheduler(data_path)
        success = scheduler.initialize_system()
        
        if success:
            return jsonify({'success': True, 'message': 'System initialized successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to initialize system'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_appointment():
    """Schedule a new appointment"""
    if request.method == 'GET':
        return render_template('schedule.html')
    
    if not scheduler:
        return jsonify({'success': False, 'message': 'System not initialized'})
    
    try:
        patient_data = request.json
        result = scheduler.schedule_appointment(patient_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get scheduling recommendations"""
    if not scheduler:
        return jsonify({'success': False, 'message': 'System not initialized'})
    
    try:
        patient_data = request.json
        recommendations = scheduler.get_schedule_recommendations(patient_data, 5)
        return jsonify({'success': True, 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/appointments')
def view_appointments():
    """View all appointments"""
    if not scheduler:
        return jsonify({'success': False, 'message': 'System not initialized'})
    
    try:
        # Get appointments from availability manager
        appointments = []
        for booking in scheduler.availability_manager.bookings:
            slot = next((s for s in scheduler.availability_manager.availability_slots 
                        if s['slot_id'] == booking['slot_id']), None)
            if slot:
                appointments.append({
                    'booking': booking,
                    'slot': slot,
                    'start_time': datetime.fromisoformat(slot['start_time']),
                    'end_time': datetime.fromisoformat(slot['start_time']) + timedelta(minutes=slot['duration_minutes'])
                })
        
        # Sort by start time
        appointments.sort(key=lambda x: x['start_time'])
        
        return render_template('appointments.html', appointments=appointments)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/analytics')
def analytics():
    """View system analytics"""
    if not scheduler:
        return jsonify({'success': False, 'message': 'System not initialized'})
    
    try:
        analytics_data = scheduler.get_system_analytics()
        return render_template('analytics.html', analytics=analytics_data)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/doctors')
def view_doctors():
    """View available doctors"""
    try:
        doctors_file = os.path.join(data_path, 'doctors.json')
        if os.path.exists(doctors_file):
            with open(doctors_file, 'r') as f:
                doctors = json.load(f)
        else:
            doctors = []
        
        return render_template('doctors.html', doctors=doctors)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(get_system_status())

def get_system_status():
    """Get current system status"""
    status = {
        'scheduling_available': SCHEDULING_AVAILABLE,
        'scheduler_initialized': scheduler is not None,
        'data_path_exists': os.path.exists(data_path),
        'models_trained': False,
        'total_appointments': 0,
        'available_slots': 0
    }
    
    if scheduler:
        try:
            # Check if models are trained
            models_path = os.path.join(data_path, 'models')
            status['models_trained'] = (
                os.path.exists(os.path.join(models_path, 'success_classifier.pkl')) and
                os.path.exists(os.path.join(models_path, 'duration_predictor.pkl'))
            )
            
            # Get appointment counts
            status['total_appointments'] = len(scheduler.availability_manager.bookings)
            status['available_slots'] = len([
                slot for slot in scheduler.availability_manager.availability_slots 
                if slot['is_available']
            ])
        except:
            pass
    
    return status

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("=" * 60)
    print("VETERINARY SCHEDULING WEB INTERFACE")
    print("=" * 60)
    print("Starting web server...")
    print("The interface will open automatically in your browser.")
    print("If it doesn't open, go to: http://127.0.0.1:5000")
    print("=" * 60)
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run Flask app
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
