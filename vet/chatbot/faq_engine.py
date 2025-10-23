"""
FAQ Engine for Veterinary Chatbot
Handles frequently asked questions with AI responses
"""

import json
import re
from typing import Dict, List, Tuple
from datetime import datetime

class FAQEngine:
    def __init__(self):
        self.faq_data = self._load_faq_data()
        self.intent_patterns = self._load_intent_patterns()
        
    def _load_faq_data(self) -> Dict:
        """Load FAQ data with categories and responses"""
        return {
            "appointments": {
                "questions": [
                    "How do I book an appointment?",
                    "Can I schedule online?",
                    "How to make appointment?",
                    "Book appointment",
                    "Schedule visit"
                ],
                "responses": [
                    "You can book an appointment by calling us at (555) 123-4567 or using our online scheduling system. Our AI-powered scheduler will find the best time slot for you and your pet.",
                    "Yes! You can schedule online 24/7 through our website. Our AI system will recommend the best available times based on your pet's needs and our doctors' availability.",
                    "To make an appointment, visit our website and use the 'Schedule Appointment' feature. Our AI will help you find the perfect time slot."
                ]
            },
            "services": {
                "questions": [
                    "What services do you offer?",
                    "What treatments are available?",
                    "Services provided",
                    "What can you do for my pet?",
                    "Available treatments"
                ],
                "responses": [
                    "We offer comprehensive veterinary services including routine checkups, vaccinations, surgery, emergency care, dental care, grooming, and specialized treatments. Our AI system can recommend the best services for your pet's specific needs.",
                    "Our services include: General Practice, Surgery, Emergency Care, Cardiology, Dermatology, Dental Care, Vaccinations, and Grooming. Each service is optimized using AI to ensure the best outcomes."
                ]
            },
            "emergency": {
                "questions": [
                    "Emergency care",
                    "My pet is sick",
                    "Urgent help needed",
                    "Pet emergency",
                    "Emergency vet"
                ],
                "responses": [
                    "For emergencies, call our emergency line at (555) 911-VET immediately. Our emergency team is available 24/7. If it's a life-threatening situation, please come to our clinic right away.",
                    "If your pet is showing signs of distress, difficulty breathing, severe injury, or unusual behavior, please contact us immediately. Our AI triage system can help assess the urgency level."
                ]
            },
            "pricing": {
                "questions": [
                    "How much does it cost?",
                    "What are your prices?",
                    "Cost of treatment",
                    "Pricing information",
                    "How much for consultation?"
                ],
                "responses": [
                    "Our pricing varies based on the service needed. Basic consultation starts at $75, vaccinations from $45, and surgery costs depend on the procedure. Contact us for a detailed quote based on your pet's specific needs.",
                    "We offer transparent pricing with no hidden fees. Our AI system can provide cost estimates based on your pet's condition and required treatments. Call us for personalized pricing information."
                ]
            },
            "hours": {
                "questions": [
                    "What are your hours?",
                    "When are you open?",
                    "Operating hours",
                    "Clinic hours",
                    "When can I visit?"
                ],
                "responses": [
                    "We're open Monday-Friday 8AM-6PM, Saturday 9AM-4PM, and Sunday 10AM-3PM. Emergency services are available 24/7. Our AI scheduling system is always online for appointment booking.",
                    "Regular hours: Mon-Fri 8AM-6PM, Sat 9AM-4PM, Sun 10AM-3PM. Emergency care is available 24/7. You can book appointments online anytime through our AI-powered system."
                ]
            },
            "vaccinations": {
                "questions": [
                    "Vaccination schedule",
                    "When to vaccinate?",
                    "Pet vaccines",
                    "Vaccination requirements",
                    "Immunization schedule"
                ],
                "responses": [
                    "Puppies and kittens need a series of vaccinations starting at 6-8 weeks. Adult pets typically need annual boosters. Our AI system can create a personalized vaccination schedule for your pet based on their age, breed, and lifestyle.",
                    "Vaccination schedules vary by pet age and species. Puppies/kittens: every 3-4 weeks until 16 weeks. Adult pets: annual boosters. Our AI can generate a custom schedule for your pet's specific needs."
                ]
            },
            "grooming": {
                "questions": [
                    "Grooming services",
                    "Pet grooming",
                    "Bathing and grooming",
                    "Nail trimming",
                    "Pet spa"
                ],
                "responses": [
                    "We offer full grooming services including bathing, brushing, nail trimming, ear cleaning, and styling. Our AI system can recommend grooming frequency based on your pet's breed and coat type.",
                    "Our grooming services include baths, nail trims, ear cleaning, teeth brushing, and breed-specific styling. We use AI to determine the best grooming schedule for your pet's health and appearance."
                ]
            },
            "general": {
                "questions": [
                    "Hello",
                    "Hi",
                    "Help",
                    "Information",
                    "General question"
                ],
                "responses": [
                    "Hello! I'm your AI veterinary assistant. I can help you with appointments, services, emergency care, pricing, and general pet health questions. How can I assist you today?",
                    "Hi there! I'm here to help with all your veterinary needs. I can schedule appointments, answer questions about our services, provide health advice, and much more. What would you like to know?"
                ]
            }
        }
    
    def _load_intent_patterns(self) -> Dict:
        """Load intent recognition patterns"""
        return {
            "appointment": [
                r"book", r"schedule", r"appointment", r"visit", r"come in",
                r"make appointment", r"set up", r"reserve"
            ],
            "emergency": [
                r"emergency", r"urgent", r"sick", r"hurt", r"injured",
                r"not well", r"critical", r"immediate"
            ],
            "pricing": [
                r"cost", r"price", r"how much", r"expensive", r"fee",
                r"charge", r"payment", r"bill"
            ],
            "services": [
                r"service", r"treatment", r"care", r"what do you do",
                r"offer", r"provide", r"available"
            ],
            "hours": [
                r"hours", r"open", r"when", r"time", r"schedule",
                r"available", r"closed"
            ],
            "vaccination": [
                r"vaccine", r"vaccination", r"shot", r"immunization",
                r"inoculation", r"preventive"
            ],
            "grooming": [
                r"groom", r"bath", r"nail", r"trim", r"clean",
                r"spa", r"beauty"
            ]
        }
    
    def find_best_response(self, user_input: str) -> Tuple[str, str, float]:
        """Find the best response for user input"""
        user_input_lower = user_input.lower()
        
        # Calculate scores for each category
        category_scores = {}
        
        for category, data in self.faq_data.items():
            score = 0
            
            # Check question patterns
            for question in data["questions"]:
                if self._calculate_similarity(user_input_lower, question.lower()) > 0.6:
                    score += 1
            
            # Check intent patterns
            if category in self.intent_patterns:
                for pattern in self.intent_patterns[category]:
                    if re.search(pattern, user_input_lower):
                        score += 0.5
            
            category_scores[category] = score
        
        # Find best category
        best_category = max(category_scores, key=category_scores.get)
        best_score = category_scores[best_category]
        
        if best_score > 0:
            # Select random response from best category
            import random
            responses = self.faq_data[best_category]["responses"]
            response = random.choice(responses)
            confidence = min(best_score / 3, 1.0)  # Normalize confidence
            
            return response, best_category, confidence
        else:
            # Default response
            return (
                "I'm not sure I understand your question. Could you please rephrase it? "
                "I can help you with appointments, services, emergency care, pricing, and general pet health questions.",
                "general",
                0.3
            )
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using simple word matching"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def get_suggested_questions(self, category: str = None) -> List[str]:
        """Get suggested questions for user"""
        if category and category in self.faq_data:
            return self.faq_data[category]["questions"][:3]
        
        # Return popular questions from all categories
        popular_questions = []
        for cat_data in self.faq_data.values():
            popular_questions.extend(cat_data["questions"][:2])
        
        return popular_questions[:6]
    
    def add_feedback(self, question: str, response: str, rating: int):
        """Add user feedback to improve responses"""
        feedback = {
            "question": question,
            "response": response,
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        }
        
        # In a real system, this would be saved to a database
        print(f"Feedback received: {feedback}")
    
    def get_analytics(self) -> Dict:
        """Get chatbot analytics"""
        return {
            "total_categories": len(self.faq_data),
            "total_questions": sum(len(cat["questions"]) for cat in self.faq_data.values()),
            "total_responses": sum(len(cat["responses"]) for cat in self.faq_data.values()),
            "categories": list(self.faq_data.keys())
        }

if __name__ == "__main__":
    # Test the FAQ engine
    faq = FAQEngine()
    
    test_questions = [
        "How do I book an appointment?",
        "What are your hours?",
        "My pet is sick, what should I do?",
        "How much does a consultation cost?",
        "Do you offer grooming services?"
    ]
    
    print("FAQ Engine Test:")
    print("=" * 50)
    
    for question in test_questions:
        response, category, confidence = faq.find_best_response(question)
        print(f"Q: {question}")
        print(f"A: {response}")
        print(f"Category: {category}, Confidence: {confidence:.2f}")
        print("-" * 30)
