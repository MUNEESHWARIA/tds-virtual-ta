from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import base64
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

# Load knowledge base
def load_knowledge_base():
    """Load knowledge base from kb.json file"""
    try:
        with open('kb.json', 'r', encoding='utf-8') as f:
            kb = json.load(f)
            logger.info(f"Loaded {len(kb)} entries from knowledge base")
            return kb
    except FileNotFoundError:
        logger.warning("kb.json not found, using default responses")
        return get_default_kb()
    except Exception as e:
        logger.error(f"Error loading knowledge base: {e}")
        return get_default_kb()

def get_default_kb():
    """Default knowledge base if file is not found"""
    return [
        {
            "keywords": ["gpt-4o-mini", "gpt-3.5-turbo", "ai", "proxy", "model"],
            "related_terms": ["openai", "api", "token", "usage"],
            "category": ["ai", "api", "assignment"],
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
            "related_terms": ["pip", "environment", "conda"],
            "category": ["python", "setup"],
            "answer": "To set up Python for TDS, install Python 3.8+, create a virtual environment, and install required packages using pip install -r requirements.txt",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                    "text": "TDS Course Forum"
                }
            ]
        }
    ]

# Load knowledge base on startup
knowledge_base = load_knowledge_base()

def find_best_answer(question, image_data=None):
    """Find the best answer for a given question"""
    try:
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
    
    except Exception as e:
        logger.error(f"Error in find_best_answer: {e}")
        return {
            "answer": "Sorry, I encountered an error processing your question. Please try again.",
            "links": []
        }

def handle_question():
    """Main question handling logic"""
    try:
        # Log the request
        logger.info(f"Received {request.method} request to {request.path}")
        
        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        # Get JSON data
        try:
            data = request.get_json(force=True)
        except Exception as e:
            logger.warning(f"Invalid JSON: {e}")
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
        
        if not data:
            return jsonify({
                "error": "No JSON data provided",
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
        
        logger.info(f"Processing question: {question[:50]}...")
        
        # Process image if provided (basic validation)
        if image_data:
            try:
                # Validate base64 image data
                base64.b64decode(image_data[:100])  # Just validate first part
                logger.info("Image data provided and validated")
            except Exception as e:
                logger.warning(f"Invalid image data: {e}")
                image_data = None
        
        # Find best answer
        result = find_best_answer(question, image_data)
        
        # Ensure proper response format
        response = {
            "answer": result.get("answer", "No answer available"),
            "links": result.get("links", [])
        }
        
        logger.info("Successfully processed question")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in handle_question: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Internal server error",
            "message": "Please try again later",
            "usage": {
                "method": "POST",
                "body": {
                    "question": "Your question here",
                    "image": "Optional base64 encoded image"
                }
            }
        }), 500

# Main API endpoint - handles both root and /api/ paths
@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def root():
    """Main endpoint for the API"""
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    elif request.method == 'POST':
        return handle_question()
    else:
        return jsonify({
            "message": "TDS Virtual TA API",
            "version": "1.0",
            "status": "running",
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
            },
            "knowledge_base_entries": len(knowledge_base)
        })

# Alternative API endpoint for backward compatibility
@app.route('/api/', methods=['GET', 'POST', 'OPTIONS'])
def api():
    """Alternative API endpoint"""
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    elif request.method == 'POST':
        return handle_question()
    else:
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

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TDS Virtual TA",
        "version": "1.0",
        "knowledge_base_entries": len(knowledge_base)
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": ["/", "/api/", "/health"]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method Not Allowed",
        "message": "This endpoint does not support the requested HTTP method",
        "supported_methods": ["GET", "POST"]
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting TDS Virtual TA on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Knowledge base entries: {len(knowledge_base)}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
