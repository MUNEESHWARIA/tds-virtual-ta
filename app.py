from flask import Flask, request, jsonify
import json
import os
import base64
from io import BytesIO
import re
from datetime import datetime

app = Flask(__name__)

# Load knowledge base
def load_knowledge_base():
    try:
        with open('kb.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

knowledge_base = load_knowledge_base()

def find_best_answer(question, image_data=None):
    """Find the best answer for a given question"""
    question_lower = question.lower()
    
    # Score each answer based on keyword matches
    best_matches = []
    
    for entry in knowledge_base:
        score = 0
        
        # Check keyword matches
        for keyword in entry.get('keywords', []):
            if keyword.lower() in question_lower:
                score += 2
        
        # Check related terms
        for term in entry.get('related_terms', []):
            if term.lower() in question_lower:
                score += 1
        
        # Boost score for category matches
        for category in entry.get('category', []):
            if category.lower() in question_lower:
                score += 1.5
        
        if score > 0:
            best_matches.append((score, entry))
    
    # Sort by score and return best match
    if best_matches:
        best_matches.sort(key=lambda x: x[0], reverse=True)
        return best_matches[0][1]
    
    # Default response if no match found
    return {
        "answer": "I don't have specific information about that topic. Please check the course materials or ask on the Discourse forum for more detailed help.",
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                "text": "TDS Discourse Forum - Ask your question here"
            }
        ]
    }

def handle_question():
    """Main question handling logic"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid JSON data",
                "usage": {
                    "method": "POST",
                    "body": {
                        "question": "Your question here",
                        "image": "Optional base64 encoded image"
                    }
                }
            }), 400
        
        question = data.get('question', '').strip()
        image_data = data.get('image', '')
        
        if not question:
            return jsonify({
                "error": "Question is required",
                "usage": {
                    "method": "POST",
                    "body": {
                        "question": "Your question here",
                        "image": "Optional base64 encoded image"
                    }
                }
            }), 400
        
        # Process image if provided (basic validation)
        if image_data:
            try:
                # Validate base64 image data
                base64.b64decode(image_data[:100])  # Just validate first part
            except:
                image_data = None
        
        # Find best answer
        result = find_best_answer(question, image_data)
        
        # Ensure proper response format
        response = {
            "answer": result.get("answer", "No answer available"),
            "links": result.get("links", [])
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "usage": {
                "method": "POST",
                "body": {
                    "question": "Your question here",
                    "image": "Optional base64 encoded image"
                }
            }
        }), 500

# Main API endpoint - handles both root and /api/ paths
@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        return handle_question()
    else:
        return jsonify({
            "message": "TDS Virtual TA API",
            "version": "1.0",
            "endpoints": {
                "GET /": "API information",
                "POST /": "Submit questions to the Virtual TA",
                "GET /health": "Health check",
                "POST /api/": "Submit questions to the Virtual TA (alternative endpoint)"
            },
            "usage": {
                "method": "POST",
                "url": "/",
                "body": {
                    "question": "Your question here",
                    "image": "Optional base64 encoded image"
                }
            }
        })

# Alternative API endpoint for backward compatibility
@app.route('/api/', methods=['POST'])
def api():
    return handle_question()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TDS Virtual TA",
        "version": "1.0"
    })

# API info endpoint
@app.route('/api/', methods=['GET'])
def api_info():
    return jsonify({
        "message": "TDS Virtual TA API",
        "version": "1.0",
        "endpoint": "/api/",
        "methods": ["POST"],
        "usage": {
            "method": "POST",
            "url": "/api/",
            "body": {
                "question": "Your question here",
                "image": "Optional base64 encoded image"
            }
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
