"""
AI-Powered Veterinary Chatbot
Main chatbot interface with natural language processing
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any
from .faq_engine import FAQEngine
from .response_generator import ResponseGenerator

class VetChatbot:
    def __init__(self):
        self.faq_engine = FAQEngine()
        self.response_generator = ResponseGenerator()
        self.conversation_history = []
        self.user_context = {}
        
    def process_message(self, user_input: str, user_id: str = "default") -> Dict[str, Any]:
        """Process user message and generate response"""
        # Clean and preprocess input
        cleaned_input = self._preprocess_input(user_input)
        
        # Get FAQ response
        faq_response, category, confidence = self.faq_engine.find_best_response(cleaned_input)
        
        # Generate enhanced response
        enhanced_response = self.response_generator.enhance_response(
            faq_response, category, user_input, self.user_context.get(user_id, {})
        )
        
        # Get suggested questions
        suggested_questions = self.faq_engine.get_suggested_questions(category)
        
        # Update conversation history
        self._update_conversation_history(user_id, user_input, enhanced_response)
        
        # Update user context
        self._update_user_context(user_id, category, user_input)
        
        # Generate response object
        response = {
            "message": enhanced_response,
            "category": category,
            "confidence": confidence,
            "suggested_questions": suggested_questions,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "conversation_id": self._get_conversation_id(user_id)
        }
        
        return response
    
    def _preprocess_input(self, user_input: str) -> str:
        """Clean and preprocess user input"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', user_input.strip())
        
        # Remove special characters but keep basic punctuation
        cleaned = re.sub(r'[^\w\s\?\!\.\,]', '', cleaned)
        
        # Convert to lowercase for processing
        return cleaned.lower()
    
    def _update_conversation_history(self, user_id: str, user_input: str, bot_response: str):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
    
    def _update_user_context(self, user_id: str, category: str, user_input: str):
        """Update user context for better responses"""
        if user_id not in self.user_context:
            self.user_context[user_id] = {}
        
        context = self.user_context[user_id]
        
        # Track user interests
        if "interests" not in context:
            context["interests"] = []
        
        if category not in context["interests"]:
            context["interests"].append(category)
        
        # Track recent topics
        if "recent_topics" not in context:
            context["recent_topics"] = []
        
        context["recent_topics"].append(category)
        if len(context["recent_topics"]) > 5:
            context["recent_topics"] = context["recent_topics"][-5:]
        
        # Extract pet information if mentioned
        pet_info = self._extract_pet_information(user_input)
        if pet_info:
            context["pet_info"] = pet_info
    
    def _extract_pet_information(self, user_input: str) -> Dict:
        """Extract pet information from user input"""
        pet_info = {}
        
        # Extract pet type
        pet_types = ["dog", "cat", "bird", "rabbit", "hamster", "fish", "reptile"]
        for pet_type in pet_types:
            if pet_type in user_input.lower():
                pet_info["type"] = pet_type
                break
        
        # Extract age information
        age_patterns = [
            r"(\d+)\s*(?:years?|months?|weeks?)\s*old",
            r"(\d+)\s*(?:year|month|week)\s*old"
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                pet_info["age"] = match.group(1)
                break
        
        # Extract symptoms or conditions
        symptoms = ["sick", "hurt", "injured", "not eating", "vomiting", "diarrhea", "lethargic"]
        mentioned_symptoms = [symptom for symptom in symptoms if symptom in user_input.lower()]
        if mentioned_symptoms:
            pet_info["symptoms"] = mentioned_symptoms
        
        return pet_info
    
    def _get_conversation_id(self, user_id: str) -> str:
        """Generate conversation ID"""
        return f"conv_{user_id}_{datetime.now().strftime('%Y%m%d')}"
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for user"""
        return self.conversation_history.get(user_id, [])
    
    def clear_conversation(self, user_id: str):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        if user_id in self.user_context:
            del self.user_context[user_id]
    
    def get_user_context(self, user_id: str) -> Dict:
        """Get user context"""
        return self.user_context.get(user_id, {})
    
    def provide_feedback(self, user_id: str, message_id: str, rating: int, feedback_text: str = ""):
        """Provide feedback on chatbot response"""
        feedback = {
            "user_id": user_id,
            "message_id": message_id,
            "rating": rating,
            "feedback_text": feedback_text,
            "timestamp": datetime.now().isoformat()
        }
        
        # In a real system, this would be saved to a database
        print(f"Feedback received: {feedback}")
        
        # Update FAQ engine with feedback
        self.faq_engine.add_feedback("", "", rating)
    
    def get_analytics(self) -> Dict:
        """Get chatbot analytics"""
        faq_analytics = self.faq_engine.get_analytics()
        
        return {
            "faq_analytics": faq_analytics,
            "active_users": len(self.conversation_history),
            "total_conversations": sum(len(conv) for conv in self.conversation_history.values()),
            "average_conversation_length": self._calculate_average_conversation_length(),
            "most_common_categories": self._get_most_common_categories()
        }
    
    def _calculate_average_conversation_length(self) -> float:
        """Calculate average conversation length"""
        if not self.conversation_history:
            return 0.0
        
        total_messages = sum(len(conv) for conv in self.conversation_history.values())
        return total_messages / len(self.conversation_history)
    
    def _get_most_common_categories(self) -> List[Tuple[str, int]]:
        """Get most common conversation categories"""
        category_counts = {}
        
        for user_id, context in self.user_context.items():
            if "recent_topics" in context:
                for topic in context["recent_topics"]:
                    category_counts[topic] = category_counts.get(topic, 0) + 1
        
        return sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    
    def generate_quick_responses(self, category: str = None) -> List[str]:
        """Generate quick response options"""
        if category:
            return self.faq_engine.get_suggested_questions(category)
        
        # Generate general quick responses
        return [
            "Book an appointment",
            "Emergency care",
            "Service information",
            "Pricing details",
            "Clinic hours",
            "Contact information"
        ]
    
    def handle_escalation(self, user_input: str) -> bool:
        """Determine if conversation should be escalated to human"""
        escalation_keywords = [
            "speak to human", "talk to person", "human agent",
            "not helpful", "doesn't work", "frustrated",
            "complaint", "problem", "issue"
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in escalation_keywords)
    
    def get_escalation_response(self) -> str:
        """Get response for escalation to human"""
        return (
            "I understand you'd like to speak with a human representative. "
            "Let me connect you with one of our veterinary staff members. "
            "Please hold while I transfer you to our team."
        )

if __name__ == "__main__":
    # Test the chatbot
    chatbot = VetChatbot()
    
    test_messages = [
        "Hello, I need to book an appointment for my dog",
        "What are your hours?",
        "My cat is sick, what should I do?",
        "How much does a consultation cost?",
        "I want to speak to a human"
    ]
    
    print("Veterinary Chatbot Test:")
    print("=" * 50)
    
    for message in test_messages:
        response = chatbot.process_message(message, "test_user")
        print(f"User: {message}")
        print(f"Bot: {response['message']}")
        print(f"Category: {response['category']}, Confidence: {response['confidence']:.2f}")
        print("-" * 30)
