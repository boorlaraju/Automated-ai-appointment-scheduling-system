"""
Training Script for Veterinary Scheduling ML Model
Generates dummy data, trains models, and saves them for production use
"""

import os
import sys
import pandas as pd
from datetime import datetime
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import DummyDataGenerator
from ml_model import SchedulingMLModel
from scheduler import AutoScheduler

def main():
    """Main training function"""
    print("=" * 60)
    print("VETERINARY SCHEDULING ML MODEL TRAINING")
    print("=" * 60)
    
    # Initialize components
    data_generator = DummyDataGenerator()
    ml_model = SchedulingMLModel()
    
    # Create data directory
    data_path = "vet/scheduling/data/"
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(os.path.join(data_path, "models"), exist_ok=True)
    
    print("\n1. Generating dummy dataset...")
    print("-" * 40)
    
    # Generate training data
    dataset = data_generator.generate_training_dataset()
    data_generator.save_doctors_data()
    
    print(f"Generated dataset with {len(dataset)} appointments")
    print(f"Dataset shape: {dataset.shape}")
    print(f"Success rate: {dataset['was_successful'].mean():.3f}")
    
    print("\n2. Training ML models...")
    print("-" * 40)
    
    # Train the models
    model_metrics = ml_model.train_models(dataset)
    
    print("\nModel Performance Metrics:")
    for metric, value in model_metrics.items():
        print(f"  {metric}: {value:.3f}")
    
    print("\n3. Feature Importance Analysis...")
    print("-" * 40)
    
    # Get feature importance
    feature_importance = ml_model.get_feature_importance()
    print("Feature Importance (Success Prediction):")
    for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {importance:.3f}")
    
    print("\n4. Testing the complete system...")
    print("-" * 40)
    
    # Initialize the complete scheduler
    scheduler = AutoScheduler(data_path)
    
    # Test scheduling
    test_patient = {
        'patient_name': 'Test Patient',
        'pet_name': 'Test Pet',
        'pet_type': 'Dog',
        'appointment_type': 'Checkup',
        'urgency': 'Medium',
        'notes': 'Test appointment'
    }
    
    print("Testing automatic scheduling...")
    result = scheduler.schedule_appointment(test_patient)
    
    if result['success']:
        print("✓ Scheduling test successful!")
        print(f"  Booked appointment: {result['booking']['booking_id']}")
        print(f"  Success probability: {result['ml_predictions']['success_probability']:.3f}")
        print(f"  Predicted duration: {result['ml_predictions']['predicted_duration']:.1f} minutes")
    else:
        print("✗ Scheduling test failed")
        print(f"  Error: {result['message']}")
    
    print("\n5. System Analytics...")
    print("-" * 40)
    
    # Get system analytics
    analytics = scheduler.get_system_analytics()
    
    print("System Performance:")
    print(f"  Total appointments: {analytics.get('total_appointments', 0)}")
    print(f"  Success rate: {analytics.get('success_rate', 0):.3f}")
    print(f"  Average duration: {analytics.get('average_duration_minutes', 0):.1f} minutes")
    
    print("\nAppointment Type Distribution:")
    for app_type, count in analytics.get('appointment_type_distribution', {}).items():
        print(f"  {app_type}: {count}")
    
    print("\n6. Saving training report...")
    print("-" * 40)
    
    # Save training report
    training_report = {
        'training_date': datetime.now().isoformat(),
        'dataset_size': len(dataset),
        'model_metrics': model_metrics,
        'feature_importance': feature_importance,
        'system_analytics': analytics,
        'test_result': result
    }
    
    with open(os.path.join(data_path, "training_report.json"), 'w') as f:
        json.dump(training_report, f, indent=2, default=str)
    
    print(f"Training report saved to {data_path}training_report.json")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nThe veterinary scheduling system is now ready for use.")
    print("You can now:")
    print("  1. Use AutoScheduler to schedule appointments")
    print("  2. Get ML-based recommendations")
    print("  3. Manage doctor availability")
    print("  4. Run automatic scheduling for patient queues")
    print("\nNext steps:")
    print("  - Integrate with your web application")
    print("  - Set up real-time data feeds")
    print("  - Configure production settings")

if __name__ == "__main__":
    main()
