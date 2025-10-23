"""
Response Generator for Veterinary Chatbot
Enhances FAQ responses with personalized and contextual information
"""

import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

class ResponseGenerator:
    def __init__(self):
        self.personalization_templates = self._load_personalization_templates()
        self.contextual_additions = self._load_contextual_additions()
        
    def _load_personalization_templates(self) -> Dict:
        """Load personalization templates for responses"""
        return {
            "appointment": [
                "I'd be happy to help you schedule an appointment! ",
                "Let me help you find the perfect time for your visit. ",
                "I can assist you with booking an appointment. "
            ],
            "emergency": [
                "I understand this is urgent. ",
                "For immediate assistance, ",
                "In case of emergency, "
            ],
            "pricing": [
                "I can provide you with detailed pricing information. ",
                "Let me give you the cost breakdown. ",
                "Here are our current rates: "
            ],
            "services": [
                "We offer a comprehensive range of services. ",
                "Our clinic provides various treatments. ",
                "Here's what we can do for your pet: "
            ],
            "general": [
                "I'm here to help! ",
                "Let me assist you with that. ",
                "I can provide you with the information you need. "
            ]
        }
    
    def _load_contextual_additions(self) -> Dict:
        """Load contextual additions based on user context"""
        return {
            "pet_info": {
                "dog": "Since you have a dog, I recommend our canine specialists who can provide breed-specific care. ",
                "cat": "For your cat, we have feline experts who understand cat behavior and health needs. ",
                "bird": "Birds require specialized care, and we have avian veterinarians on staff. ",
                "rabbit": "Rabbits have unique health requirements, and our exotic pet specialists can help. ",
                "hamster": "Small pets like hamsters need gentle, specialized care. ",
                "fish": "Aquatic pets require special attention, and we have fish health experts. ",
                "reptile": "Reptiles have specific environmental and health needs that our exotic pet vets understand. "
            },
            "time_context": {
                "morning": "Good morning! ",
                "afternoon": "Good afternoon! ",
                "evening": "Good evening! ",
                "night": "I see you're reaching out late - for emergencies, we're available 24/7. "
            },
            "urgency": {
                "high": "I can see this is urgent. ",
                "medium": "I understand this is important. ",
                "low": "I'm here to help with your question. "
            }
        }
    
    def enhance_response(self, base_response: str, category: str, user_input: str, user_context: Dict) -> str:
        """Enhance base response with personalization and context"""
        enhanced_response = base_response
        
        # Add personalization based on category
        if category in self.personalization_templates:
            template = random.choice(self.personalization_templates[category])
            enhanced_response = template + enhanced_response
        
        # Add contextual information based on user context
        enhanced_response = self._add_contextual_info(enhanced_response, user_context)
        
        # Add time-based context
        enhanced_response = self._add_time_context(enhanced_response)
        
        # Add urgency context
        enhanced_response = self._add_urgency_context(enhanced_response, user_input)
        
        # Add pet-specific information
        enhanced_response = self._add_pet_specific_info(enhanced_response, user_context)
        
        # Add call-to-action
        enhanced_response = self._add_call_to_action(enhanced_response, category)
        
        return enhanced_response
    
    def _add_contextual_info(self, response: str, user_context: Dict) -> str:
        """Add contextual information based on user context"""
        if "pet_info" in user_context:
            pet_info = user_context["pet_info"]
            if "type" in pet_info and pet_info["type"] in self.contextual_additions["pet_info"]:
                pet_context = self.contextual_additions["pet_info"][pet_info["type"]]
                response = pet_context + response
        
        return response
    
    def _add_time_context(self, response: str) -> str:
        """Add time-based context to response"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            time_context = self.contextual_additions["time_context"]["morning"]
        elif 12 <= current_hour < 17:
            time_context = self.contextual_additions["time_context"]["afternoon"]
        elif 17 <= current_hour < 22:
            time_context = self.contextual_additions["time_context"]["evening"]
        else:
            time_context = self.contextual_additions["time_context"]["night"]
        
        return time_context + response
    
    def _add_urgency_context(self, response: str, user_input: str) -> str:
        """Add urgency context based on user input"""
        urgent_keywords = ["emergency", "urgent", "immediate", "critical", "sick", "hurt", "injured"]
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in urgent_keywords):
            urgency_context = self.contextual_additions["urgency"]["high"]
        elif any(word in user_input_lower for word in ["important", "need", "require"]):
            urgency_context = self.contextual_additions["urgency"]["medium"]
        else:
            urgency_context = self.contextual_additions["urgency"]["low"]
        
        return urgency_context + response
    
    def _add_pet_specific_info(self, response: str, user_context: Dict) -> str:
        """Add pet-specific information to response"""
        if "pet_info" in user_context:
            pet_info = user_context["pet_info"]
            
            # Add age-specific information
            if "age" in pet_info:
                age = int(pet_info["age"])
                if age < 1:
                    response += " Since your pet is young, they may need more frequent checkups and vaccinations. "
                elif age > 7:
                    response += " For senior pets, we recommend regular health monitoring and preventive care. "
            
            # Add symptom-specific information
            if "symptoms" in pet_info:
                symptoms = pet_info["symptoms"]
                if "sick" in symptoms or "not eating" in symptoms:
                    response += " If your pet is showing signs of illness, it's important to seek veterinary care promptly. "
                elif "hurt" in symptoms or "injured" in symptoms:
                    response += " For injuries, please bring your pet in for immediate evaluation. "
        
        return response
    
    def _add_call_to_action(self, response: str, category: str) -> str:
        """Add appropriate call-to-action based on category"""
        call_to_actions = {
            "appointment": " Would you like me to help you schedule an appointment now?",
            "emergency": " Please call our emergency line at (555) 911-VET if this is urgent.",
            "pricing": " Would you like me to provide more detailed pricing information?",
            "services": " Would you like to know more about any specific service?",
            "hours": " You can also book appointments online 24/7 through our website.",
            "vaccination": " Would you like me to create a vaccination schedule for your pet?",
            "grooming": " Would you like to schedule a grooming appointment?",
            "general": " Is there anything else I can help you with today?"
        }
        
        if category in call_to_actions:
            response += call_to_actions[category]
        
        return response
    
    def generate_follow_up_questions(self, category: str, user_context: Dict) -> List[str]:
        """Generate follow-up questions based on category and context"""
        follow_up_templates = {
            "appointment": [
                "What type of appointment do you need?",
                "Do you have a preferred doctor?",
                "What's your pet's name and type?",
                "When would be a good time for you?"
            ],
            "emergency": [
                "What symptoms is your pet showing?",
                "How long has this been going on?",
                "Is your pet eating and drinking normally?",
                "Are there any visible injuries?"
            ],
            "pricing": [
                "What specific service are you interested in?",
                "Do you have pet insurance?",
                "Would you like a detailed cost breakdown?",
                "Are you looking for a payment plan?"
            ],
            "services": [
                "What type of pet do you have?",
                "What specific care does your pet need?",
                "Are you looking for routine or specialized care?",
                "Do you have any health concerns about your pet?"
            ]
        }
        
        if category in follow_up_templates:
            return follow_up_templates[category][:3]  # Return top 3 questions
        
        return ["Is there anything else I can help you with?"]
    
    def generate_quick_actions(self, category: str) -> List[Dict[str, str]]:
        """Generate quick action buttons based on category"""
        quick_actions = {
            "appointment": [
                {"text": "Book Now", "action": "book_appointment"},
                {"text": "View Availability", "action": "check_availability"},
                {"text": "Emergency Booking", "action": "emergency_booking"}
            ],
            "emergency": [
                {"text": "Call Emergency Line", "action": "call_emergency"},
                {"text": "Get Directions", "action": "get_directions"},
                {"text": "Check Wait Times", "action": "check_wait_times"}
            ],
            "pricing": [
                {"text": "Get Quote", "action": "get_quote"},
                {"text": "View Services", "action": "view_services"},
                {"text": "Insurance Info", "action": "insurance_info"}
            ],
            "services": [
                {"text": "View All Services", "action": "view_all_services"},
                {"text": "Find Specialist", "action": "find_specialist"},
                {"text": "Schedule Consultation", "action": "schedule_consultation"}
            ]
        }
        
        return quick_actions.get(category, [
            {"text": "More Help", "action": "more_help"},
            {"text": "Contact Us", "action": "contact_us"},
            {"text": "Visit Website", "action": "visit_website"}
        ])
    
    def generate_escalation_response(self, reason: str) -> str:
        """Generate response for escalation to human"""
        escalation_responses = {
            "complex_question": "I understand you have a complex question that requires human expertise. Let me connect you with one of our veterinary professionals.",
            "technical_issue": "I apologize for any technical difficulties. Let me transfer you to our support team who can better assist you.",
            "complaint": "I'm sorry to hear about your concern. Let me connect you with our management team who can address this properly.",
            "emergency": "This sounds like an emergency situation. Let me immediately connect you with our emergency veterinary team.",
            "general": "I understand you'd prefer to speak with a human. Let me connect you with one of our veterinary staff members."
        }
        
        return escalation_responses.get(reason, escalation_responses["general"])

if __name__ == "__main__":
    # Test the response generator
    generator = ResponseGenerator()
    
    # Test enhancement
    base_response = "You can book an appointment by calling us or using our online system."
    enhanced = generator.enhance_response(
        base_response, 
        "appointment", 
        "I need to book an appointment for my sick dog", 
        {"pet_info": {"type": "dog", "symptoms": ["sick"]}}
    )
    
    print("Response Enhancement Test:")
    print("=" * 50)
    print(f"Original: {base_response}")
    print(f"Enhanced: {enhanced}")
    print("=" * 50)
