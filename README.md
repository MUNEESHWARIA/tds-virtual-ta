# TDS Virtual TA 🧠🤖

An automated teaching assistant for IIT Madras' Tools in Data Science course that answers student questions based on course content and Discourse posts.

## 🚀 Features

- **Smart Question Answering**: Uses keyword matching and semantic understanding to provide relevant answers
- **Image Support**: Accepts base64-encoded images (with basic processing)
- **Comprehensive Knowledge Base**: Covers TDS topics including Python, assignments, APIs, deployment, etc.
- **RESTful API**: Clean JSON API for easy integration
- **Health Monitoring**: Built-in health check endpoint
- **Discourse Scraping**: Advanced scraper with date range support

## 📡 API Usage

### Endpoint: `POST /api/`

**Request Format:**
```json
{
  "question": "Should I use gpt-4o-mini or gpt3.5 turbo?",
  "image": "optional_base64_encoded_image"
}
```

**Response Format:**
```json
{
  "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
      "text": "Use the model that's mentioned in the question."
    }
  ]
}
```

### Example with cURL:
```bash
curl "https://your-app.railway.app/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I setup Python for TDS?"}'
```

### Other Endpoints:
- `GET /health` - Health check
- `GET /` - API information

## 🏗️ Local Development

### Prerequisites
- Python 3.8+
- Git

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/MUNEESHWARIA/tds-virtual-ta.git
   cd tds-virtual-ta
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Test the API:**
   ```bash
   python test_api.py http://localhost:5000
   ```

## 🚀 Deployment Options

### Option 1: Railway (Recommended)

1. **Push to GitHub** (ensure your repo is public)

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway will auto-detect and deploy your Flask app

3. **Configure Environment:**
   - Railway automatically sets the `PORT` environment variable
   - Your app will be available at `https://your-app-name.up.railway.app`

4. **Update promptfoo config:**
   ```yaml
   providers:
     - provider: rest
       config:
         url: "https://your-app-name.up.railway.app/api/"
   ```

### Option 2: Render

1. **Create account on [render.com](https://render.com)**

2. **Create new Web Service:**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app.py`

### Option 3: Heroku

1. **Install Heroku CLI and login**

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 🕷️ Web Scraping

### Basic Usage:
```bash
# Scrape posts by ID range
python scraper.py --start-id 1 --end-id 100

# Scrape posts by date range
python scraper.py --start-date "2025-01-01" --end-date "2025-04-14" --category "tds"

# Custom output file
python scraper.py --start-id 1 --end-id 50 --output "my_posts.json"
```

### Advanced Options:
- `--delay`: Set delay between requests (default: 1 second)
- `--category`: Specify Discourse category (default: "tds")
- `--output`: Output filename (default: "scraped_posts.json")

## 🧪 Testing

### Run Tests:
```bash
# Test local instance
python test_api.py

# Test deployed instance
python test_api.py https://your-app.railway.app
```

### Test with promptfoo:
```bash
# Install promptfoo
npm install -g promptfoo

# Update config with your URL
# Edit project-tds-virtual-ta-promptfoo.yaml

# Run evaluation
npx promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

## 📁 Project Structure

```
tds-virtual-ta/
├── app.py                 # Main Flask application
├── kb.json               # Knowledge base with Q&A pairs
├── scraper.py            # Advanced Discourse scraper
├── test_api.py           # API testing script
├── requirements.txt      # Python dependencies
├── LICENSE              # MIT License
├── README.md            # This file
├── Procfile             # For Railway/Heroku deployment
├── railway.json         # Railway configuration
└── project-tds-virtual-ta-promptfoo.yaml  # Evaluation config
```

## 🔧 Configuration

### Environment Variables:
- `PORT`: Server port (default: 5000)

### Knowledge Base:
Edit `kb.json` to add new Q&A pairs:
```json
{
  "keywords": ["python", "setup"],
  "related_terms": ["install", "environment"],
  "category": ["python", "setup"],
  "answer": "Your answer here...",
  "links": [
    {
      "url": "https://example.com",
      "text": "Link description"
    }
  ]
}
```

## 🎯 Evaluation Criteria

- **Functionality**: API responds correctly to POST requests
- **Knowledge Coverage**: Handles diverse TDS-related questions
- **Response Quality**: Provides relevant answers with supporting links
- **Performance**: Responds within 30 seconds
- **Deployment**: Publicly accessible URL
- **Code Quality**: Clean, documented code with MIT license

## 🏆 Bonus Points

- ✅ **Discourse Scraper**: Advanced scraper with date range support
- 🎯 **Production Ready**: Error handling, health checks, proper logging
- 📚 **Comprehensive KB**: Covers wide range of TDS topics

## 🐛 Troubleshooting

### Common Issues:

1. **"TypeError: Failed to fetch"**
   - Check if your deployed URL is accessible
   - Verify the API endpoint accepts POST requests
   - Test with curl or test script

2. **Import Errors**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

3. **Deployment Issues**
   - Verify Procfile/start command is correct
   - Check application logs on hosting platform
   - Ensure PORT environment variable is used

### Testing Your Deployment:
```bash
# Quick test
curl https://your-app.railway.app/health

# Full API test
curl "https://your-app.railway.app/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions about the TDS course or this project:
- Visit the [TDS Discourse Forum](https://discourse.onlinedegree.iitm.ac.in/c/tds/)
- Check course materials and announcements

---

**Note**: This is a project submission for IIT Madras' Tools in Data Science course. Make sure your deployment is accessible before the evaluation deadline!
