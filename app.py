from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import base64
import io
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Load knowledge base
try:
    with open("kb.json", "r", encoding="utf-8") as f:
        kb = json.load(f)
except FileNotFoundError:
    kb = []

def process_image(image_data):
    """Process base64 image data - placeholder for OCR/image analysis"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        # For now, just return a generic response about images
        return "I can see you've shared an image. Please describe what specific help you need with it."
    except:
        return "Unable to process the image. Please try again or describe your question in text."

def find_best_answer(question, image_context=None):
    """Find the best answer using improved matching"""
    question_lower = question.lower()
    
    # Check for exact keyword matches first
    best_match = None
    max_score = 0
    
    for item in kb:
        score = 0
        
        # Check keyword matches
        for keyword in item.get("keywords", []):
            if keyword.lower() in question_lower:
                score += 2
        
        # Check for partial matches in question content
        if any(word in question_lower for word in item.get("related_terms", [])):
            score += 1
            
        # Check category matches
        if item.get("category") and any(cat in question_lower for cat in item.get("category", [])):
            score += 1
            
        if score > max_score:
            max_score = score
            best_match = item
    
    if best_match:
        return best_match
    
    # Fallback: check for common question patterns
    fallback_responses = {
        "assignment": {
            "answer": "For assignment-related questions, please check the course materials and Discourse for specific guidelines. Make sure to follow the submission format and deadlines.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                    "text": "TDS Course Discussion Forum"
                }
            ]
        },
        "grading": {
            "answer": "Grading information can be found in the course handbook. For specific grading queries, please post on Discourse with your question details.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                    "text": "TDS Course Discussion Forum"
                }
            ]
        },
        "python": {
            "answer": "For Python-related questions, refer to the course materials and practice notebooks. Make sure you have the required libraries installed.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                    "text": "TDS Course Discussion Forum"
                }
            ]
        }
    }
    
    for pattern, response in fallback_responses.items():
        if pattern in question_lower:
            return response
    
    return None

@app.route("/api/", methods=["POST"])
def virtual_ta():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        question = data.get("question", "").strip()
        image_data = data.get("image", "")
        
        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400
        
        # Process image if provided
        image_context = None
        if image_data:
            image_context = process_image(image_data)
        
        # Find best answer
        result = find_best_answer(question, image_context)
        
        if result:
            response = {
                "answer": result["answer"],
                "links": result.get("links", [])
            }
            
            # Add image context if available
            if image_context and "I can see you've shared an image" in image_context:
                response["answer"] += f"\n\nRegarding your image: {image_context}"
            
            return jsonify(response)
        else:
            return jsonify({
                "answer": "I don't have specific information about that topic yet. Please check the course materials on Discourse or ask a more specific question.",
                "links": [
                    {
                        "url": "https://discourse.onlinedegree.iitm.ac.in/c/tds/",
                        "text": "TDS Course Discussion Forum"
                    }
                ]
            })
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "kb_entries": len(kb)
    })

@app.route("/", methods=["GET"])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "TDS Virtual TA API",
        "version": "1.0",
        "endpoints": {
            "POST /api/": "Submit questions to the Virtual TA",
            "GET /health": "Health check",
            "GET /": "API information"
        },
        "usage": {
            "method": "POST",
            "url": "/api/",
            "body": {
                "question": "Your question here",
                "image": "Optional base64 encoded image"
            }
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
