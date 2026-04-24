# 🤖 TDS Virtual Teaching Assistant

An AI-powered Virtual Teaching Assistant developed as part of my Diploma in Data Science. This project answers student queries using course content and discussion forum data, providing accurate and context-aware responses.

---

## 📌 Overview

The TDS Virtual Teaching Assistant is designed to simulate an intelligent assistant that helps students by answering their academic questions. It leverages Large Language Models (LLMs) along with retrieved data from course materials and Discourse forums.

---

## 🚀 Features

* ✅ Automated question-answering system
* ✅ Context-aware responses using LLMs
* ✅ FastAPI-based REST API
* ✅ Web scraping from discussion forums
* ✅ Supports structured JSON responses
* ✅ Optional image-based query handling
* ✅ Deployed using Docker and Railway

---

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Backend Framework:** FastAPI
* **AI Model:** OpenAI API (LLM)
* **Data Collection:** Web Scraping (Discourse)
* **Deployment:** Docker, Railway

---

## 📂 Project Structure

```
tds-virtual-ta/
│── app/                # Main application code
│── data/               # Scraped/processed data
│── main.py             # FastAPI entry point
│── requirements.txt    # Dependencies
│── Dockerfile          # Container setup
│── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/MUNEESHWARIA/tds-virtual-ta.git
cd tds-virtual-ta
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file and add:

```
OPENAI_API_KEY=your_api_key_here
```

### 4. Run the application

```
uvicorn main:app --reload
```

---

## 🔗 API Usage

### Endpoint

```
POST /api
```

### Sample Request

```json
{
  "question": "What is overfitting in machine learning?",
  "image": null
}
```

### Sample Response

```json
{
  "answer": "Overfitting occurs when a model learns the training data too well, including noise, and performs poorly on new data.",
  "links": [
    {
      "url": "https://example.com",
      "text": "Reference Material"
    }
  ]
}
```

---

## 📸 Demo / Output

*Add screenshots of your API response or UI here for better presentation.*

---

## 🌐 Deployment

The application is containerized using Docker and deployed on Railway for public access.

---

## 📚 Learning Outcomes

* Built an end-to-end AI-powered application
* Learned API development using FastAPI
* Implemented data scraping and preprocessing
* Worked with LLMs for real-world applications
* Understood cloud deployment and containerization

---

## 📌 Future Improvements

* Add frontend interface for better usability
* Improve retrieval accuracy with embeddings
* Enhance support for image-based queries
* Optimize response time

---

## 👩‍💻 Author

**Muneeshwari N**
Aspiring Data Scientist

GitHub: https://github.com/MUNEESHWARIA

---

## 📄 License

This project is licensed under the MIT License.
