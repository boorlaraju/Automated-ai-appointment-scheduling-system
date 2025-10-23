"""
Analytics Engine for Veterinary Inventory
Provides insights into sales patterns, expiry tracking, and recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json
import os

class InventoryAnalytics:
    def __init__(self, data_path: str = "vet/inventory/data/"):
        self.data_path = data_path
        self.medicines_file = os.path.join(data_path, "medicines.json")
        self.transactions_file = os.path.join(data_path, "transactions.json")
        
    def load_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Load medicines and transactions data"""
        medicines = []
        transactions = []
        
        if os.path.exists(self.medicines_file):
            with open(self.medicines_file, 'r') as f:
                medicines = json.load(f)
        
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as f:
                transactions = json.load(f)
        
        return medicines, transactions
    
    def get_sales_analytics(self, days: int = 30) -> Dict:
        """Get comprehensive sales analytics"""
        medicines, transactions = self.load_data()
        
        # Filter transactions for the specified period
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_transactions = [
            t for t in transactions 
            if datetime.fromisoformat(t["transaction_date"]) >= cutoff_date
        ]
        
        # Calculate metrics
        total_revenue = sum(t["total_amount"] for t in recent_transactions)
        total_quantity_sold = sum(t["quantity"] for t in recent_transactions)
        unique_medicines_sold = len(set(t["medicine_id"] for t in recent_transactions))
        
        # Daily sales trend
        daily_sales = {}
        for transaction in recent_transactions:
            date = datetime.fromisoformat(transaction["transaction_date"]).date()
            if date not in daily_sales:
                daily_sales[date] = {"revenue": 0, "quantity": 0}
            daily_sales[date]["revenue"] += transaction["total_amount"]
            daily_sales[date]["quantity"] += transaction["quantity"]
        
        # Category analysis
        category_sales = {}
        for transaction in recent_transactions:
            medicine_id = transaction["medicine_id"]
            medicine = next((m for m in medicines if m["id"] == medicine_id), None)
            if medicine:
                category = medicine["category"]
                if category not in category_sales:
                    category_sales[category] = {"revenue": 0, "quantity": 0}
                category_sales[category]["revenue"] += transaction["total_amount"]
                category_sales[category]["quantity"] += transaction["quantity"]
        
        return {
            "period_days": days,
            "total_revenue": total_revenue,
            "total_quantity_sold": total_quantity_sold,
            "unique_medicines_sold": unique_medicines_sold,
            "average_daily_revenue": total_revenue / days if days > 0 else 0,
            "daily_sales": daily_sales,
            "category_breakdown": category_sales,
            "top_selling_medicines": self._get_top_selling_medicines(medicines, recent_transactions, 10),
            "low_selling_medicines": self._get_low_selling_medicines(medicines, recent_transactions, 10)
        }
    
    def get_expiry_analytics(self) -> Dict:
        """Get expiry date analytics"""
        medicines, _ = self.load_data()
        
        current_date = datetime.now()
        expiring_30_days = []
        expiring_60_days = []
        expiring_90_days = []
        expired = []
        
        for medicine in medicines:
            if medicine["expiry_date"]:
                try:
                    expiry_date = datetime.fromisoformat(medicine["expiry_date"])
                    days_until_expiry = (expiry_date - current_date).days
                    
                    if days_until_expiry < 0:
                        expired.append(medicine)
                    elif days_until_expiry <= 30:
                        expiring_30_days.append(medicine)
                    elif days_until_expiry <= 60:
                        expiring_60_days.append(medicine)
                    elif days_until_expiry <= 90:
                        expiring_90_days.append(medicine)
                except:
                    continue
        
        # Calculate total value of expiring medicines
        def calculate_value(medicine_list):
            return sum(m["quantity"] * m["unit_price"] for m in medicine_list)
        
        return {
            "expired": {
                "count": len(expired),
                "value": calculate_value(expired),
                "medicines": expired
            },
            "expiring_30_days": {
                "count": len(expiring_30_days),
                "value": calculate_value(expiring_30_days),
                "medicines": expiring_30_days
            },
            "expiring_60_days": {
                "count": len(expiring_60_days),
                "value": calculate_value(expiring_60_days),
                "medicines": expiring_60_days
            },
            "expiring_90_days": {
                "count": len(expiring_90_days),
                "value": calculate_value(expiring_90_days),
                "medicines": expiring_90_days
            }
        }
    
    def get_stock_analytics(self) -> Dict:
        """Get stock level analytics"""
        medicines, _ = self.load_data()
        
        # Stock level categories
        out_of_stock = [m for m in medicines if m["quantity"] == 0]
        low_stock = [m for m in medicines if 0 < m["quantity"] <= 10]
        medium_stock = [m for m in medicines if 10 < m["quantity"] <= 50]
        high_stock = [m for m in medicines if m["quantity"] > 50]
        
        # Calculate total values
        def calculate_value(medicine_list):
            return sum(m["quantity"] * m["unit_price"] for m in medicine_list)
        
        total_inventory_value = calculate_value(medicines)
        
        return {
            "total_medicines": len(medicines),
            "total_inventory_value": total_inventory_value,
            "out_of_stock": {
                "count": len(out_of_stock),
                "medicines": out_of_stock
            },
            "low_stock": {
                "count": len(low_stock),
                "value": calculate_value(low_stock),
                "medicines": low_stock
            },
            "medium_stock": {
                "count": len(medium_stock),
                "value": calculate_value(medium_stock),
                "medicines": medium_stock
            },
            "high_stock": {
                "count": len(high_stock),
                "value": calculate_value(high_stock),
                "medicines": high_stock
            }
        }
    
    def get_category_analytics(self) -> Dict:
        """Get analytics by medicine category"""
        medicines, transactions = self.load_data()
        
        # Group medicines by category
        categories = {}
        for medicine in medicines:
            category = medicine["category"]
            if category not in categories:
                categories[category] = {
                    "medicines": [],
                    "total_quantity": 0,
                    "total_value": 0
                }
            
            categories[category]["medicines"].append(medicine)
            categories[category]["total_quantity"] += medicine["quantity"]
            categories[category]["total_value"] += medicine["quantity"] * medicine["unit_price"]
        
        # Calculate sales for each category
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_transactions = [
            t for t in transactions 
            if datetime.fromisoformat(t["transaction_date"]) >= cutoff_date
        ]
        
        for transaction in recent_transactions:
            medicine_id = transaction["medicine_id"]
            medicine = next((m for m in medicines if m["id"] == medicine_id), None)
            if medicine:
                category = medicine["category"]
                if "sales" not in categories[category]:
                    categories[category]["sales"] = {"quantity": 0, "revenue": 0}
                categories[category]["sales"]["quantity"] += transaction["quantity"]
                categories[category]["sales"]["revenue"] += transaction["total_amount"]
        
        return categories
    
    def get_trend_analysis(self, days: int = 90) -> Dict:
        """Get trend analysis for sales and inventory"""
        medicines, transactions = self.load_data()
        
        # Get daily sales data
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_transactions = [
            t for t in transactions 
            if datetime.fromisoformat(t["transaction_date"]) >= cutoff_date
        ]
        
        # Group by date
        daily_data = {}
        for transaction in recent_transactions:
            date = datetime.fromisoformat(transaction["transaction_date"]).date()
            if date not in daily_data:
                daily_data[date] = {"revenue": 0, "quantity": 0, "transactions": 0}
            daily_data[date]["revenue"] += transaction["total_amount"]
            daily_data[date]["quantity"] += transaction["quantity"]
            daily_data[date]["transactions"] += 1
        
        # Calculate trends
        dates = sorted(daily_data.keys())
        if len(dates) >= 7:
            # Weekly trend
            recent_week = dates[-7:]
            previous_week = dates[-14:-7] if len(dates) >= 14 else dates[-7:]
            
            recent_week_revenue = sum(daily_data[date]["revenue"] for date in recent_week)
            previous_week_revenue = sum(daily_data[date]["revenue"] for date in previous_week)
            
            revenue_trend = ((recent_week_revenue - previous_week_revenue) / previous_week_revenue * 100) if previous_week_revenue > 0 else 0
        else:
            revenue_trend = 0
        
        return {
            "period_days": days,
            "daily_data": daily_data,
            "revenue_trend_percentage": revenue_trend,
            "average_daily_revenue": sum(daily_data[date]["revenue"] for date in daily_data) / len(daily_data) if daily_data else 0,
            "average_daily_quantity": sum(daily_data[date]["quantity"] for date in daily_data) / len(daily_data) if daily_data else 0
        }
    
    def get_recommendations(self) -> Dict:
        """Get AI-powered recommendations for inventory management"""
        medicines, transactions = self.load_data()
        
        recommendations = {
            "reorder_suggestions": [],
            "expiry_alerts": [],
            "slow_moving_items": [],
            "fast_moving_items": [],
            "cost_optimization": []
        }
        
        # Reorder suggestions
        for medicine in medicines:
            if medicine["quantity"] <= 10:
                # Calculate average monthly sales
                sales_history = [
                    t for t in transactions 
                    if t["medicine_id"] == medicine["id"] and 
                    datetime.fromisoformat(t["transaction_date"]) >= datetime.now() - timedelta(days=30)
                ]
                monthly_sales = sum(t["quantity"] for t in sales_history)
                
                recommendations["reorder_suggestions"].append({
                    "medicine_id": medicine["id"],
                    "medicine_name": medicine["name"],
                    "current_stock": medicine["quantity"],
                    "monthly_sales": monthly_sales,
                    "recommended_quantity": max(50, monthly_sales * 2),
                    "urgency": "High" if medicine["quantity"] <= 5 else "Medium"
                })
        
        # Expiry alerts
        current_date = datetime.now()
        for medicine in medicines:
            if medicine["expiry_date"]:
                try:
                    expiry_date = datetime.fromisoformat(medicine["expiry_date"])
                    days_until_expiry = (expiry_date - current_date).days
                    
                    if days_until_expiry <= 30:
                        recommendations["expiry_alerts"].append({
                            "medicine_id": medicine["id"],
                            "medicine_name": medicine["name"],
                            "expiry_date": medicine["expiry_date"],
                            "days_until_expiry": days_until_expiry,
                            "current_stock": medicine["quantity"],
                            "urgency": "High" if days_until_expiry <= 7 else "Medium"
                        })
                except:
                    continue
        
        # Slow moving items
        cutoff_date = datetime.now() - timedelta(days=60)
        medicine_sales = {}
        for transaction in transactions:
            if datetime.fromisoformat(transaction["transaction_date"]) >= cutoff_date:
                medicine_id = transaction["medicine_id"]
                if medicine_id not in medicine_sales:
                    medicine_sales[medicine_id] = 0
                medicine_sales[medicine_id] += transaction["quantity"]
        
        for medicine in medicines:
            sales_quantity = medicine_sales.get(medicine["id"], 0)
            if sales_quantity < 5 and medicine["quantity"] > 20:  # Low sales but high stock
                recommendations["slow_moving_items"].append({
                    "medicine_id": medicine["id"],
                    "medicine_name": medicine["name"],
                    "current_stock": medicine["quantity"],
                    "sales_last_60_days": sales_quantity,
                    "suggestion": "Consider promotional pricing or review if still needed"
                })
        
        return recommendations
    
    def _get_top_selling_medicines(self, medicines: List[Dict], transactions: List[Dict], limit: int) -> List[Dict]:
        """Get top selling medicines"""
        medicine_sales = {}
        
        for transaction in transactions:
            medicine_id = transaction["medicine_id"]
            if medicine_id not in medicine_sales:
                medicine_sales[medicine_id] = {"quantity": 0, "revenue": 0}
            medicine_sales[medicine_id]["quantity"] += transaction["quantity"]
            medicine_sales[medicine_id]["revenue"] += transaction["total_amount"]
        
        # Sort by quantity sold
        sorted_sales = sorted(medicine_sales.items(), key=lambda x: x[1]["quantity"], reverse=True)
        
        result = []
        for medicine_id, sales_data in sorted_sales[:limit]:
            medicine = next((m for m in medicines if m["id"] == medicine_id), None)
            if medicine:
                result.append({
                    "medicine_id": medicine_id,
                    "medicine_name": medicine["name"],
                    "category": medicine["category"],
                    "quantity_sold": sales_data["quantity"],
                    "revenue": sales_data["revenue"]
                })
        
        return result
    
    def _get_low_selling_medicines(self, medicines: List[Dict], transactions: List[Dict], limit: int) -> List[Dict]:
        """Get low selling medicines"""
        medicine_sales = {}
        
        for transaction in transactions:
            medicine_id = transaction["medicine_id"]
            if medicine_id not in medicine_sales:
                medicine_sales[medicine_id] = 0
            medicine_sales[medicine_id] += transaction["quantity"]
        
        # Get all medicines with their sales data
        all_medicines = []
        for medicine in medicines:
            sales_quantity = medicine_sales.get(medicine["id"], 0)
            all_medicines.append({
                "medicine_id": medicine["id"],
                "medicine_name": medicine["name"],
                "category": medicine["category"],
                "quantity_sold": sales_quantity,
                "current_stock": medicine["quantity"]
            })
        
        # Sort by quantity sold (ascending)
        all_medicines.sort(key=lambda x: x["quantity_sold"])
        
        return all_medicines[:limit]

if __name__ == "__main__":
    # Test the analytics engine
    analytics = InventoryAnalytics()
    
    # Test sales analytics
    sales_data = analytics.get_sales_analytics(30)
    print(f"Sales Analytics: {sales_data}")
    
    # Test expiry analytics
    expiry_data = analytics.get_expiry_analytics()
    print(f"Expiry Analytics: {expiry_data}")
    
    # Test recommendations
    recommendations = analytics.get_recommendations()
    print(f"Recommendations: {recommendations}")
