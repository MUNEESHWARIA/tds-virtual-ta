from flask import Flask, request, jsonify
import os
import json
import base64
from io import BytesIO
import re

app = Flask(__name__)

# Load knowledge base
def load_knowledge_base():
    try:
        with open('kb.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback knowledge base if file doesn't exist
        return [
            {
                "keywords": ["gpt", "model", "ai", "proxy"],
                "related_terms": ["gpt-4o-mini", "gpt-3.5-turbo", "openai"],
                "category": ["ai", "model"],
                "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
                "links": [
                    {
                        "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                        "text": "Use the model that's mentioned in the question."
                    }
                ]
            },
            {
                "keywords": ["python", "setup", "install"],
                "related_terms": ["environment", "pip", "conda"],
                "category": ["python", "setup"],
                "answer": "To set up Python for TDS, install Python 3.8+, create a virtual environment, and install required packages using pip install -r requirements.txt",
                "links": [
                    {
                        "url": "https://discourse.onlinedegree.iitm.ac.in/t/python-setup-guide/123",
                        "text": "Python Setup Guide for TDS"
                    }
                ]
            }
        ]

knowledge_base = load_knowledge_base()

def find_answer(question, image=None):
    """Find the best answer for a given question"""
    question_lower = question.lower()
    
    # Score each knowledge base entry
    best_match = None
    best_score = 0
    
    for entry in knowledge_base:
        score = 0
        
        # Score based on keywords
        for keyword in entry.get('keywords', []):
            if keyword.lower() in question_lower:
                score += 3
        
        # Score based on related terms
        for term in entry.get('related_terms', []):
            if term.lower() in question_lower:
                score += 2
        
        # Score based on category
        for cat in entry.get('category', []):
            if cat.lower() in question_lower:
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = entry
    
    if best_match:
        return {
            "answer": best_match.get('answer', 'I found some information but cannot provide a specific answer.'),
            "links": best_match.get('links', [])
        }
    else:
        # Default fallback answer
        return {
            "answer": "I don't have specific information about this topic in my knowledge base. Please refer to the course materials or ask on the TDS Discourse forum for more help.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                    "text": "TDS Discourse Forum"
                }
            ]
        }

@app.route('/', methods=['GET', 'POST'])
def api_endpoint():
    """Main API endpoint that handles both GET and POST requests"""
    
    if request.method == 'GET':
        return jsonify({
            "message": "TDS Virtual TA API is running",
            "usage": "Send POST request with JSON containing 'question' and optional 'image' (base64)",
            "example": {
                "question": "How do I setup Python for TDS?",
                "image": "optional_base64_encoded_image"
            }
        })
    
    elif request.method == 'POST':
        try:
            # Get JSON data from request
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "error": "No JSON data provided"
                }), 400
            
            question = data.get('question', '').strip()
            image = data.get('image', None)
            
            if not question:
                return jsonify({
                    "error": "Question field is required"
                }), 400
            
            # Process the image if provided (basic validation)
            if image:
                try:
                    # Validate base64 format
                    base64.b64decode(image[:100])  # Just validate first 100 chars
                except Exception:
                    return jsonify({
                        "error": "Invalid base64 image format"
                    }), 400
            
            # Find answer
            result = find_answer(question, image)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                "error": f"Internal server error: {str(e)}"
            }), 500

@app.route('/api/', methods=['GET', 'POST'])
def api_endpoint_alt():
    """Alternative API endpoint for /api/ path"""
    return api_endpoint()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "TDS Virtual TA is running properly"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "Use POST / or POST /api/ with JSON data containing 'question' field"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "message": "Use POST method with JSON data"
    }), 405

if __name__ == '__main__':
    # Use PORT environment variable if available (for Railway/Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
