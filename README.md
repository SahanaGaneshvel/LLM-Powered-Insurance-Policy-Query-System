# LLM-Powered Insurance Policy Query System

An AI-powered system that processes insurance policy documents and answers natural language queries using advanced LLM technology.

## Features

- **Document Processing**: PDF, DOCX, and email files
- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered Answers**: Uses Groq LLM for intelligent responses
- **Vector Search**: Pinecone-based semantic document retrieval
- **Web Interface**: Modern, responsive UI
- **RESTful API**: Programmatic access

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

### 3. Run the Application

**Web Interface (Recommended):**
```bash
python start_ui.py
```
Access at: `http://localhost:8080`

**API Server:**
```bash
python start.py
```
Access at: `http://localhost:8000`

### 4. Deploy to Railway

**Install Railway CLI:**
```bash
npm install -g @railway/cli
```

**Login and Deploy:**
```bash
railway login
railway up
```

**Set Environment Variables in Railway Dashboard:**
- `GROQ_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_ENVIRONMENT`

## API Usage

### Authentication
All endpoints require Bearer token:
```
Authorization: Bearer 4a7809a665f2f39b1f2fa7c7073518e6baa4ebe9309eea30dae92adba5772c
```

### Main Endpoint
```bash
POST /hackrx/run
```

**Request:**
```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

**Response:**
```json
{
  "answers": [
    "The grace period is 30 days...",
    "There is a 36-month waiting period..."
  ]
}
```

### Other Endpoints
- `GET /health` - System status
- `POST /api/v1/process-single` - Single query processing
- `GET /api/v1/stats` - System statistics
- `DELETE /api/v1/clear-index` - Clear vector index

## Testing with Postman

1. **Health Check**: `GET http://localhost:8000/health`
2. **Main Processing**: `POST http://localhost:8000/hackrx/run`
3. **Single Query**: `POST http://localhost:8000/api/v1/process-single`

## Troubleshooting

- **Import Errors**: Run `pip install -r requirements.txt`
- **API Key Errors**: Verify environment variables in `.env`
- **Document Issues**: Ensure URL is accessible and format is supported
- **Performance**: Check logs in `logs/` directory

## Project Structure

```
├── app.py                 # API server
├── ui_server.py           # Web UI server
├── api_routes.py          # API endpoints
├── document_parser.py     # Document processing
├── embedding_service.py   # Vector embeddings
├── groq_service.py       # LLM integration
├── utils.py              # Utilities
├── start.py              # API launcher
├── start_ui.py           # UI launcher
└── ui.html               # Web interface
```

## License

MIT License

---

**Built with FastAPI, Groq, and Pinecone**