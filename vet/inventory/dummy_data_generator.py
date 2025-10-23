"""
Dummy Data Generator for Veterinary Inventory
Generates realistic inventory data for testing and development
"""

import random
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os

class InventoryDataGenerator:
    def __init__(self):
        self.medicine_categories = [
            "Antibiotics", "Pain Relief", "Vaccines", "Supplements", 
            "Dermatology", "Cardiology", "Dental", "Emergency", 
            "Surgery", "Diagnostics", "Grooming", "Behavioral"
        ]
        
        self.medicine_types = [
            "Tablet", "Capsule", "Liquid", "Injection", "Cream", 
            "Ointment", "Spray", "Drops", "Powder", "Gel"
        ]
        
        self.manufacturers = [
            "VetPharma Inc", "Animal Health Corp", "PetCare Solutions",
            "Veterinary Specialties", "Animal Wellness Co", "PetMed Pro",
            "VetCare International", "Animal Therapeutics", "PetHealth Ltd"
        ]
        
        self.suppliers = [
            "MedSupply Direct", "VetWholesale", "Animal Care Distributors",
            "PetMed Supply", "Veterinary Solutions", "Animal Health Partners"
        ]
        
        self.storage_conditions = [
            "Room Temperature", "Refrigerated", "Frozen", "Controlled Temperature",
            "Dry Storage", "Light Sensitive", "Humidity Controlled"
        ]
        
        self.dosage_forms = [
            "Tablet", "Capsule", "Liquid", "Injection", "Cream", "Ointment",
            "Spray", "Drops", "Powder", "Gel", "Paste", "Chewable"
        ]
        
        self.medicine_names = {
            "Antibiotics": [
                "Amoxicillin 250mg", "Cephalexin 500mg", "Doxycycline 100mg",
                "Enrofloxacin 50mg", "Metronidazole 250mg", "Clindamycin 150mg",
                "Azithromycin 250mg", "Ciprofloxacin 250mg", "Penicillin G 400mg"
            ],
            "Pain Relief": [
                "Meloxicam 7.5mg", "Carprofen 25mg", "Firocoxib 57mg",
                "Tramadol 50mg", "Gabapentin 100mg", "Aspirin 81mg",
                "Ibuprofen 200mg", "Acetaminophen 500mg", "Ketoprofen 50mg"
            ],
            "Vaccines": [
                "Rabies Vaccine", "DHPP Vaccine", "Bordetella Vaccine",
                "Lyme Disease Vaccine", "Feline Leukemia Vaccine", "Canine Influenza Vaccine",
                "Feline Distemper Vaccine", "Kennel Cough Vaccine", "Leptospirosis Vaccine"
            ],
            "Supplements": [
                "Glucosamine 500mg", "Chondroitin 400mg", "Omega-3 Fish Oil",
                "Probiotics Blend", "Vitamin B Complex", "Calcium Supplement",
                "Iron Supplement", "Multivitamin", "Joint Support Formula"
            ],
            "Dermatology": [
                "Hydrocortisone Cream", "Antifungal Ointment", "Antibacterial Shampoo",
                "Medicated Wipes", "Skin Soothing Gel", "Anti-itch Spray",
                "Ear Cleaner", "Paw Balm", "Hot Spot Treatment"
            ],
            "Cardiology": [
                "Enalapril 5mg", "Furosemide 20mg", "Digoxin 0.25mg",
                "Atenolol 25mg", "Spironolactone 25mg", "Pimobendan 5mg",
                "Diltiazem 30mg", "Amlodipine 2.5mg", "Carvedilol 3.125mg"
            ]
        }
        
        self.indications = [
            "Bacterial infections", "Pain management", "Inflammation", "Allergic reactions",
            "Digestive issues", "Respiratory problems", "Skin conditions", "Joint health",
            "Immune support", "Preventive care", "Post-surgical care", "Chronic conditions"
        ]
        
        self.contraindications = [
            "Pregnancy", "Lactation", "Liver disease", "Kidney disease",
            "Heart conditions", "Allergic reactions", "Drug interactions",
            "Age restrictions", "Breed specific", "Concurrent medications"
        ]
        
        self.side_effects = [
            "Nausea", "Vomiting", "Diarrhea", "Drowsiness", "Loss of appetite",
            "Allergic reactions", "Skin irritation", "Digestive upset",
            "Behavioral changes", "Lethargy", "Increased thirst", "Urination changes"
        ]
    
    def generate_medicines(self, count: int = 100) -> List[Dict]:
        """Generate dummy medicine data"""
        medicines = []
        
        for i in range(count):
            category = random.choice(self.medicine_categories)
            medicine_name = random.choice(self.medicine_names.get(category, ["Generic Medicine"]))
            
            # Generate expiry date (1-3 years from now)
            expiry_days = random.randint(365, 1095)
            expiry_date = datetime.now() + timedelta(days=expiry_days)
            
            # Generate batch number
            batch_number = f"B{random.randint(1000, 9999)}{random.choice(['A', 'B', 'C'])}"
            
            # Generate quantity (0-200)
            quantity = random.randint(0, 200)
            
            # Generate unit price ($1-$100)
            unit_price = round(random.uniform(1.0, 100.0), 2)
            
            # Generate strength
            strength_options = ["50mg", "100mg", "250mg", "500mg", "1g", "2.5mg", "5mg", "10mg", "25mg"]
            strength = random.choice(strength_options)
            
            # Generate indications (1-3)
            num_indications = random.randint(1, 3)
            selected_indications = random.sample(self.indications, num_indications)
            
            # Generate contraindications (0-2)
            num_contraindications = random.randint(0, 2)
            selected_contraindications = random.sample(self.contraindications, num_contraindications)
            
            # Generate side effects (1-4)
            num_side_effects = random.randint(1, 4)
            selected_side_effects = random.sample(self.side_effects, num_side_effects)
            
            medicine = {
                "id": i + 1,
                "name": medicine_name,
                "generic_name": medicine_name.split()[0] if " " in medicine_name else medicine_name,
                "category": category,
                "type": "Medicine",
                "manufacturer": random.choice(self.manufacturers),
                "batch_number": batch_number,
                "quantity": quantity,
                "unit": "units",
                "unit_price": unit_price,
                "expiry_date": expiry_date.isoformat(),
                "supplier": random.choice(self.suppliers),
                "storage_conditions": random.choice(self.storage_conditions),
                "prescription_required": random.choice([True, False]),
                "dosage_form": random.choice(self.dosage_forms),
                "strength": strength,
                "indications": selected_indications,
                "contraindications": selected_contraindications,
                "side_effects": selected_side_effects,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "Active"
            }
            
            medicines.append(medicine)
        
        return medicines
    
    def generate_transactions(self, medicines: List[Dict], count: int = 500) -> List[Dict]:
        """Generate dummy transaction data"""
        transactions = []
        
        transaction_types = ["sale", "purchase", "adjustment", "return", "dispensed"]
        
        for i in range(count):
            # Random medicine
            medicine = random.choice(medicines)
            medicine_id = medicine["id"]
            
            # Random transaction type
            transaction_type = random.choice(transaction_types)
            
            # Generate quantity (1-50)
            quantity = random.randint(1, 50)
            
            # Generate unit price (slightly different from medicine price)
            base_price = medicine["unit_price"]
            price_variation = random.uniform(0.8, 1.2)
            unit_price = round(base_price * price_variation, 2)
            
            # Generate transaction date (last 90 days)
            days_ago = random.randint(0, 90)
            transaction_date = datetime.now() - timedelta(days=days_ago)
            
            # Generate customer/patient IDs
            customer_id = random.randint(1000, 9999)
            patient_id = random.randint(2000, 9999)
            
            # Generate prescription ID for dispensed items
            prescription_id = random.randint(3000, 9999) if transaction_type == "dispensed" else None
            
            # Generate notes
            notes_options = [
                "Regular prescription", "Emergency supply", "Bulk purchase",
                "Return due to expiry", "Inventory adjustment", "Sample provided",
                "Emergency dispense", "Regular refill", "New prescription"
            ]
            notes = random.choice(notes_options)
            
            transaction = {
                "id": i + 1,
                "medicine_id": medicine_id,
                "type": transaction_type,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": round(quantity * unit_price, 2),
                "customer_id": customer_id,
                "patient_id": patient_id,
                "prescription_id": prescription_id,
                "notes": notes,
                "transaction_date": transaction_date.isoformat(),
                "created_by": random.choice(["Dr. Smith", "Dr. Johnson", "Dr. Brown", "system", "admin"]),
                "status": "completed"
            }
            
            transactions.append(transaction)
        
        return transactions
    
    def generate_sales_patterns(self, medicines: List[Dict], days: int = 30) -> Dict:
        """Generate realistic sales patterns"""
        patterns = {}
        
        for medicine in medicines:
            medicine_id = medicine["id"]
            category = medicine["category"]
            
            # Different sales patterns by category
            if category == "Antibiotics":
                daily_sales = random.randint(2, 8)  # High demand
            elif category == "Pain Relief":
                daily_sales = random.randint(1, 5)  # Medium demand
            elif category == "Vaccines":
                daily_sales = random.randint(0, 3)  # Lower, seasonal
            elif category == "Supplements":
                daily_sales = random.randint(1, 4)  # Steady demand
            else:
                daily_sales = random.randint(0, 3)  # Variable demand
            
            # Generate sales for each day
            daily_transactions = []
            for day in range(days):
                date = datetime.now() - timedelta(days=day)
                
                # Random sales for the day
                num_sales = random.randint(0, daily_sales)
                for _ in range(num_sales):
                    quantity = random.randint(1, 5)
                    unit_price = medicine["unit_price"] * random.uniform(0.9, 1.1)
                    
                    daily_transactions.append({
                        "date": date.isoformat(),
                        "quantity": quantity,
                        "unit_price": round(unit_price, 2),
                        "total_amount": round(quantity * unit_price, 2)
                    })
            
            patterns[medicine_id] = daily_transactions
        
        return patterns
    
    def save_dummy_data(self, medicines: List[Dict], transactions: List[Dict], data_path: str = "vet/inventory/data/"):
        """Save dummy data to files"""
        os.makedirs(data_path, exist_ok=True)
        
        # Save medicines
        with open(os.path.join(data_path, "medicines.json"), 'w') as f:
            json.dump(medicines, f, indent=2)
        
        # Save transactions
        with open(os.path.join(data_path, "transactions.json"), 'w') as f:
            json.dump(transactions, f, indent=2)
        
        # Save sales patterns
        sales_patterns = self.generate_sales_patterns(medicines)
        with open(os.path.join(data_path, "sales_patterns.json"), 'w') as f:
            json.dump(sales_patterns, f, indent=2)
        
        print(f"Saved {len(medicines)} medicines and {len(transactions)} transactions to {data_path}")
    
    def generate_inventory_report(self, medicines: List[Dict], transactions: List[Dict]) -> Dict:
        """Generate comprehensive inventory report"""
        total_medicines = len(medicines)
        total_value = sum(m["quantity"] * m["unit_price"] for m in medicines)
        
        # Category breakdown
        categories = {}
        for medicine in medicines:
            category = medicine["category"]
            if category not in categories:
                categories[category] = {"count": 0, "value": 0}
            categories[category]["count"] += 1
            categories[category]["value"] += medicine["quantity"] * medicine["unit_price"]
        
        # Stock levels
        out_of_stock = len([m for m in medicines if m["quantity"] == 0])
        low_stock = len([m for m in medicines if 0 < m["quantity"] <= 10])
        medium_stock = len([m for m in medicines if 10 < m["quantity"] <= 50])
        high_stock = len([m for m in medicines if m["quantity"] > 50])
        
        # Expiry analysis
        current_date = datetime.now()
        expiring_30_days = len([m for m in medicines if m["expiry_date"] and 
                               datetime.fromisoformat(m["expiry_date"]) <= current_date + timedelta(days=30)])
        expired = len([m for m in medicines if m["expiry_date"] and 
                      datetime.fromisoformat(m["expiry_date"]) < current_date])
        
        # Sales analysis
        total_transactions = len(transactions)
        total_revenue = sum(t["total_amount"] for t in transactions)
        
        return {
            "summary": {
                "total_medicines": total_medicines,
                "total_inventory_value": round(total_value, 2),
                "total_transactions": total_transactions,
                "total_revenue": round(total_revenue, 2)
            },
            "categories": categories,
            "stock_levels": {
                "out_of_stock": out_of_stock,
                "low_stock": low_stock,
                "medium_stock": medium_stock,
                "high_stock": high_stock
            },
            "expiry_analysis": {
                "expiring_30_days": expiring_30_days,
                "expired": expired
            }
        }

if __name__ == "__main__":
    # Generate dummy data
    generator = InventoryDataGenerator()
    
    print("Generating dummy inventory data...")
    medicines = generator.generate_medicines(100)
    transactions = generator.generate_transactions(medicines, 500)
    
    # Save data
    generator.save_dummy_data(medicines, transactions)
    
    # Generate report
    report = generator.generate_inventory_report(medicines, transactions)
    print("\nInventory Report:")
    print("=" * 50)
    print(f"Total Medicines: {report['summary']['total_medicines']}")
    print(f"Total Value: ${report['summary']['total_inventory_value']}")
    print(f"Total Transactions: {report['summary']['total_transactions']}")
    print(f"Total Revenue: ${report['summary']['total_revenue']}")
    print(f"Out of Stock: {report['stock_levels']['out_of_stock']}")
    print(f"Low Stock: {report['stock_levels']['low_stock']}")
    print(f"Expiring in 30 days: {report['expiry_analysis']['expiring_30_days']}")
    print(f"Expired: {report['expiry_analysis']['expired']}")
    
    print("\nCategory Breakdown:")
    for category, data in report['categories'].items():
        print(f"  {category}: {data['count']} items, ${data['value']:.2f}")
