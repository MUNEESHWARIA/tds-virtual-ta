# TDS Virtual TA 🧠🤖

An automated teaching assistant for IITM's Data Science course.

## 🔧 Features
- Answers questions based on TDS course & Discourse posts
- Accepts base64 images (placeholder support)
- Simple keyword matching (can be replaced by embeddings)
- API hosted on Railway

## 📡 API Usage

**POST** `/api/` with JSON:

```json
{
  "question": "Should I use gpt-4o-mini or gpt3.5 turbo?"
}
```

**Response:**
```json
{
  "answer": "...",
  "links": [...]
}
```

## 🚀 Deploy on Railway

1. Push this repo to GitHub
2. Go to [https://railway.app](https://railway.app)
3. "New Project" → "Deploy from GitHub"
4. Set Start Command to `python app.py`

## 📜 License

MIT License