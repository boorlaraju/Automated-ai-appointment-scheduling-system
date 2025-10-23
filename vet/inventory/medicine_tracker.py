"""
Medicine Tracker for Veterinary Inventory
Tracks all types of medicines, vaccines, and medical supplies
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random
import os

class MedicineTracker:
    def __init__(self, data_path: str = "vet/inventory/data/"):
        self.data_path = data_path
        self.medicines_file = os.path.join(data_path, "medicines.json")
        self.transactions_file = os.path.join(data_path, "transactions.json")
        self.medicines = []
        self.transactions = []
        self.load_data()
        
    def load_data(self):
        """Load medicines and transaction data"""
        os.makedirs(self.data_path, exist_ok=True)
        
        # Load medicines
        if os.path.exists(self.medicines_file):
            with open(self.medicines_file, 'r') as f:
                self.medicines = json.load(f)
        else:
            self.medicines = []
        
        # Load transactions
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as f:
                self.transactions = json.load(f)
        else:
            self.transactions = []
    
    def save_data(self):
        """Save medicines and transaction data"""
        with open(self.medicines_file, 'w') as f:
            json.dump(self.medicines, f, indent=2)
        
        with open(self.transactions_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def add_medicine(self, medicine_data: Dict) -> Dict:
        """Add a new medicine to inventory"""
        medicine = {
            "id": len(self.medicines) + 1,
            "name": medicine_data.get("name", ""),
            "generic_name": medicine_data.get("generic_name", ""),
            "category": medicine_data.get("category", "General"),
            "type": medicine_data.get("type", "Medicine"),
            "manufacturer": medicine_data.get("manufacturer", ""),
            "batch_number": medicine_data.get("batch_number", ""),
            "quantity": medicine_data.get("quantity", 0),
            "unit": medicine_data.get("unit", "units"),
            "unit_price": medicine_data.get("unit_price", 0.0),
            "expiry_date": medicine_data.get("expiry_date", ""),
            "supplier": medicine_data.get("supplier", ""),
            "storage_conditions": medicine_data.get("storage_conditions", "Room Temperature"),
            "prescription_required": medicine_data.get("prescription_required", True),
            "dosage_form": medicine_data.get("dosage_form", "Tablet"),
            "strength": medicine_data.get("strength", ""),
            "indications": medicine_data.get("indications", []),
            "contraindications": medicine_data.get("contraindications", []),
            "side_effects": medicine_data.get("side_effects", []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "Active"
        }
        
        self.medicines.append(medicine)
        self.save_data()
        return medicine
    
    def update_medicine(self, medicine_id: int, update_data: Dict) -> bool:
        """Update medicine information"""
        for medicine in self.medicines:
            if medicine["id"] == medicine_id:
                medicine.update(update_data)
                medicine["updated_at"] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def get_medicine(self, medicine_id: int) -> Optional[Dict]:
        """Get medicine by ID"""
        for medicine in self.medicines:
            if medicine["id"] == medicine_id:
                return medicine
        return None
    
    def search_medicines(self, query: str, category: str = None) -> List[Dict]:
        """Search medicines by name, generic name, or category"""
        results = []
        query_lower = query.lower()
        
        for medicine in self.medicines:
            if (query_lower in medicine["name"].lower() or 
                query_lower in medicine["generic_name"].lower() or
                query_lower in medicine["category"].lower()):
                
                if category is None or medicine["category"] == category:
                    results.append(medicine)
        
        return results
    
    def get_medicines_by_category(self, category: str) -> List[Dict]:
        """Get all medicines in a specific category"""
        return [medicine for medicine in self.medicines if medicine["category"] == category]
    
    def get_low_stock_medicines(self, threshold: int = 10) -> List[Dict]:
        """Get medicines with low stock"""
        return [medicine for medicine in self.medicines if medicine["quantity"] <= threshold]
    
    def get_expiring_medicines(self, days_ahead: int = 30) -> List[Dict]:
        """Get medicines expiring within specified days"""
        expiring = []
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        for medicine in self.medicines:
            if medicine["expiry_date"]:
                try:
                    expiry_date = datetime.fromisoformat(medicine["expiry_date"])
                    if expiry_date <= cutoff_date:
                        expiring.append(medicine)
                except:
                    continue
        
        return expiring
    
    def get_expired_medicines(self) -> List[Dict]:
        """Get expired medicines"""
        expired = []
        current_date = datetime.now()
        
        for medicine in self.medicines:
            if medicine["expiry_date"]:
                try:
                    expiry_date = datetime.fromisoformat(medicine["expiry_date"])
                    if expiry_date < current_date:
                        expired.append(medicine)
                except:
                    continue
        
        return expired
    
    def add_transaction(self, transaction_data: Dict) -> Dict:
        """Add a new transaction (sale, purchase, adjustment)"""
        transaction = {
            "id": len(self.transactions) + 1,
            "medicine_id": transaction_data.get("medicine_id"),
            "type": transaction_data.get("type", "sale"),  # sale, purchase, adjustment, return
            "quantity": transaction_data.get("quantity", 0),
            "unit_price": transaction_data.get("unit_price", 0.0),
            "total_amount": transaction_data.get("quantity", 0) * transaction_data.get("unit_price", 0.0),
            "customer_id": transaction_data.get("customer_id"),
            "patient_id": transaction_data.get("patient_id"),
            "prescription_id": transaction_data.get("prescription_id"),
            "notes": transaction_data.get("notes", ""),
            "transaction_date": transaction_data.get("transaction_date", datetime.now().isoformat()),
            "created_by": transaction_data.get("created_by", "system"),
            "status": "completed"
        }
        
        self.transactions.append(transaction)
        
        # Update medicine quantity
        self._update_medicine_quantity(transaction)
        
        self.save_data()
        return transaction
    
    def _update_medicine_quantity(self, transaction: Dict):
        """Update medicine quantity based on transaction"""
        medicine_id = transaction["medicine_id"]
        quantity_change = transaction["quantity"]
        
        if transaction["type"] in ["sale", "dispensed"]:
            quantity_change = -quantity_change  # Reduce stock for sales
        elif transaction["type"] in ["purchase", "restock"]:
            quantity_change = quantity_change  # Increase stock for purchases
        
        for medicine in self.medicines:
            if medicine["id"] == medicine_id:
                medicine["quantity"] = max(0, medicine["quantity"] + quantity_change)
                medicine["updated_at"] = datetime.now().isoformat()
                break
    
    def get_medicine_sales_history(self, medicine_id: int, days: int = 30) -> List[Dict]:
        """Get sales history for a specific medicine"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        sales = []
        for transaction in self.transactions:
            if (transaction["medicine_id"] == medicine_id and 
                transaction["type"] in ["sale", "dispensed"] and
                datetime.fromisoformat(transaction["transaction_date"]) >= cutoff_date):
                sales.append(transaction)
        
        return sales
    
    def get_top_selling_medicines(self, limit: int = 10, days: int = 30) -> List[Dict]:
        """Get top selling medicines"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Calculate sales for each medicine
        medicine_sales = {}
        
        for transaction in self.transactions:
            if (transaction["type"] in ["sale", "dispensed"] and
                datetime.fromisoformat(transaction["transaction_date"]) >= cutoff_date):
                
                medicine_id = transaction["medicine_id"]
                if medicine_id not in medicine_sales:
                    medicine_sales[medicine_id] = {
                        "medicine_id": medicine_id,
                        "total_quantity": 0,
                        "total_revenue": 0.0,
                        "transaction_count": 0
                    }
                
                medicine_sales[medicine_id]["total_quantity"] += transaction["quantity"]
                medicine_sales[medicine_id]["total_revenue"] += transaction["total_amount"]
                medicine_sales[medicine_id]["transaction_count"] += 1
        
        # Sort by total quantity sold
        sorted_sales = sorted(medicine_sales.values(), key=lambda x: x["total_quantity"], reverse=True)
        
        # Add medicine details
        result = []
        for sale in sorted_sales[:limit]:
            medicine = self.get_medicine(sale["medicine_id"])
            if medicine:
                sale["medicine_name"] = medicine["name"]
                sale["category"] = medicine["category"]
                result.append(sale)
        
        return result
    
    def get_low_selling_medicines(self, limit: int = 10, days: int = 30) -> List[Dict]:
        """Get low selling medicines"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get all medicines
        all_medicines = {medicine["id"]: medicine for medicine in self.medicines}
        
        # Calculate sales for each medicine
        medicine_sales = {}
        
        for transaction in self.transactions:
            if (transaction["type"] in ["sale", "dispensed"] and
                datetime.fromisoformat(transaction["transaction_date"]) >= cutoff_date):
                
                medicine_id = transaction["medicine_id"]
                if medicine_id not in medicine_sales:
                    medicine_sales[medicine_id] = 0
                medicine_sales[medicine_id] += transaction["quantity"]
        
        # Find medicines with low or no sales
        low_selling = []
        for medicine_id, medicine in all_medicines.items():
            sales_quantity = medicine_sales.get(medicine_id, 0)
            low_selling.append({
                "medicine_id": medicine_id,
                "medicine_name": medicine["name"],
                "category": medicine["category"],
                "quantity_sold": sales_quantity,
                "current_stock": medicine["quantity"],
                "expiry_date": medicine["expiry_date"]
            })
        
        # Sort by quantity sold (ascending)
        low_selling.sort(key=lambda x: x["quantity_sold"])
        
        return low_selling[:limit]
    
    def get_inventory_summary(self) -> Dict:
        """Get inventory summary statistics"""
        total_medicines = len(self.medicines)
        total_value = sum(medicine["quantity"] * medicine["unit_price"] for medicine in self.medicines)
        
        low_stock_count = len(self.get_low_stock_medicines())
        expiring_count = len(self.get_expiring_medicines())
        expired_count = len(self.get_expired_medicines())
        
        # Category breakdown
        categories = {}
        for medicine in self.medicines:
            category = medicine["category"]
            if category not in categories:
                categories[category] = {"count": 0, "value": 0}
            categories[category]["count"] += 1
            categories[category]["value"] += medicine["quantity"] * medicine["unit_price"]
        
        return {
            "total_medicines": total_medicines,
            "total_value": total_value,
            "low_stock_count": low_stock_count,
            "expiring_count": expiring_count,
            "expired_count": expired_count,
            "categories": categories,
            "last_updated": datetime.now().isoformat()
        }
    
    def generate_reorder_recommendations(self) -> List[Dict]:
        """Generate reorder recommendations based on stock levels and sales"""
        recommendations = []
        
        for medicine in self.medicines:
            if medicine["quantity"] <= 10:  # Low stock threshold
                # Calculate average monthly sales
                sales_history = self.get_medicine_sales_history(medicine["id"], 30)
                monthly_sales = sum(sale["quantity"] for sale in sales_history)
                
                # Calculate recommended reorder quantity
                recommended_quantity = max(50, monthly_sales * 2)  # 2 months supply
                
                recommendations.append({
                    "medicine_id": medicine["id"],
                    "medicine_name": medicine["name"],
                    "current_stock": medicine["quantity"],
                    "monthly_sales": monthly_sales,
                    "recommended_quantity": recommended_quantity,
                    "urgency": "High" if medicine["quantity"] <= 5 else "Medium",
                    "estimated_cost": recommended_quantity * medicine["unit_price"]
                })
        
        return sorted(recommendations, key=lambda x: x["urgency"])

if __name__ == "__main__":
    # Test the medicine tracker
    tracker = MedicineTracker()
    
    # Test adding a medicine
    medicine_data = {
        "name": "Amoxicillin 250mg",
        "generic_name": "Amoxicillin",
        "category": "Antibiotics",
        "type": "Medicine",
        "manufacturer": "Generic Pharma",
        "quantity": 100,
        "unit_price": 2.50,
        "expiry_date": "2025-12-31",
        "prescription_required": True
    }
    
    medicine = tracker.add_medicine(medicine_data)
    print(f"Added medicine: {medicine['name']}")
    
    # Test inventory summary
    summary = tracker.get_inventory_summary()
    print(f"Inventory summary: {summary}")
