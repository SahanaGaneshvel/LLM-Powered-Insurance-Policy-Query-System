# LLM-Powered Insurance Policy Query System

A sophisticated document analysis and question-answering system designed for insurance policy processing. This application leverages advanced AI technologies to extract, analyze, and provide intelligent responses to queries about insurance documents.

## Overview

The system processes insurance policy documents (PDF, DOCX, email formats) and enables natural language querying to extract relevant information. It combines document parsing, vector embeddings, semantic search, and large language model processing to deliver accurate, contextual responses.

## Key Features

- **Multi-format Document Processing**: Supports PDF, DOCX, and email files
- **Natural Language Querying**: Process questions in plain English
- **AI-Powered Analysis**: Utilizes Groq LLM for intelligent response generation
- **Vector-based Search**: Pinecone integration for semantic document retrieval
- **Web Interface**: Modern, responsive user interface
- **RESTful API**: Comprehensive API for programmatic access
- **Performance Monitoring**: Built-in analytics and performance tracking

## System Architecture

```
User Query → Document Parser → Embedding Service → Vector Search → LLM Processing → Response
     ↓              ↓                ↓                ↓              ↓
  Web UI ← API Server ← Structured Response ← Groq LLM ← Relevant Clauses ← Pinecone
```

## Project Structure

```
LLM-Powered Insurance Policy Query System/
├── Core Application
│   ├── app.py                 # Main API server
│   ├── ui_server.py           # Web UI server
│   ├── api_routes.py          # API endpoint handlers
│   └── ui.html               # Web interface
│
├── Service Modules
│   ├── document_parser.py     # Document processing engine
│   ├── embedding_service.py   # Vector embeddings and search
│   ├── groq_service.py       # LLM integration and processing
│   └── utils.py              # Utility functions and helpers
│
├── Startup Scripts
│   ├── start.py              # API server launcher
│   └── start_ui.py           # UI server launcher
│
├── Documentation
│   ├── UI_README.md          # UI usage documentation
│   └── env_example.txt       # Environment configuration template
│
├── Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .gitignore           # Version control exclusions
│   └── __init__.py          # Package initialization
│
└── Data Directories
    ├── logs/                 # Application logs
    ├── cache/               # Cache storage
    └── temp/                # Temporary files
```

## Prerequisites

- Python 3.11 or higher
- Git version control
- Internet connection for API services

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LLM-Powered-Insurance-Policy-Query-System
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the environment template and configure your API keys:

```bash
cp env_example.txt .env
```

Edit the `.env` file with your service credentials:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# Optional Configuration
REDIS_URL=your_redis_url
```

## API Key Setup

### Groq API
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file

### Pinecone
1. Visit [Pinecone Console](https://app.pinecone.io/)
2. Create an account and set up a project
3. Note your API key and environment
4. Add both to your `.env` file

## Usage

### Web Interface (Recommended)

Launch the web interface for the best user experience:

```bash
python start_ui.py
```

Access the interface at: `http://localhost:8080`

### API Server Only

For programmatic access, start the API server:

```bash
python start.py
```

API endpoints available at: `http://localhost:8000`

### Direct Python Integration

```python
from document_parser import DocumentParser
from embedding_service import EmbeddingService
from groq_service import GroqService

# Initialize services
parser = DocumentParser()
embedding_service = EmbeddingService()
groq_service = GroqService()

# Process document
chunks = await parser.process_document_from_url("path/to/document.pdf")
await embedding_service.index_documents(chunks)

# Query document
answer = await groq_service.generate_detailed_answer(
    "What is the grace period?", 
    relevant_texts
)
```

## API Reference

### Authentication

All API endpoints require Bearer token authentication:

```
Authorization: Bearer 4a7809a665f2f39b1f2fa7c7073518e6baa4ebe9309eea30dae92adba5772d8c
```

### Endpoints

#### Health Check
```
GET /health
```
Returns system status and environment configuration.

#### Main Processing
```
POST /hackrx/run
```
Process documents and queries with the following request format:

```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

#### Single Query Processing
```
POST /api/v1/process-single
```
Process a single query with detailed response:

```json
{
  "document_url": "https://example.com/policy.pdf",
  "question": "What is the grace period?"
}
```

#### System Statistics
```
GET /api/v1/stats
```
Returns performance metrics and system statistics.

#### Clear Index
```
DELETE /api/v1/clear-index
```
Clears the vector database index.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for LLM processing | Yes | - |
| `PINECONE_API_KEY` | Pinecone API key for vector storage | Yes | - |
| `PINECONE_ENVIRONMENT` | Pinecone environment | Yes | - |
| `REDIS_URL` | Redis URL for caching | No | - |

### Performance Settings

The system is optimized for:
- **Response Time**: 2-3 seconds average
- **Document Processing**: < 1 second
- **Vector Search**: < 0.3 seconds
- **LLM Generation**: < 1.5 seconds

## Testing

### Postman Collection

1. **Health Check**: `GET http://localhost:8000/health`
2. **Main Processing**: `POST http://localhost:8000/hackrx/run`
3. **Single Query**: `POST http://localhost:8000/api/v1/process-single`
4. **Statistics**: `GET http://localhost:8000/api/v1/stats`

### Sample Test Data

**Document URLs:**
- Public insurance policy PDFs
- Government insurance documents
- Sample policy documents

**Test Questions:**
- "What is the grace period for premium payment?"
- "What is the waiting period for pre-existing diseases?"
- "What is covered under maternity benefits?"
- "What is the sum insured amount?"
- "What are the exclusions in this policy?"

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Verify Python version is 3.11+

2. **API Key Errors**
   - Verify environment variables are set correctly
   - Check API key permissions and quotas

3. **Document Processing Issues**
   - Ensure document URL is accessible
   - Verify document format is supported (PDF/DOCX)

4. **Performance Issues**
   - Monitor system resources
   - Check network connectivity
   - Verify API rate limits

### Logs and Debugging

Application logs are stored in the `logs/` directory. Enable debug mode:

```bash
export LOG_LEVEL=DEBUG
python start_ui.py
```

## Security

- **Authentication**: Bearer token required for API access
- **Input Validation**: All requests are sanitized and validated
- **Error Handling**: Sensitive information is not logged
- **HTTPS**: Recommended for production deployments

## Performance Monitoring

The system includes built-in monitoring for:
- Request processing times
- Error rates and types
- Cache hit rates
- API response times

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For technical support:
1. Review the troubleshooting section
2. Check logs in the `logs/` directory
3. Create an issue in the repository

---

**Built with FastAPI, Groq, Pinecone, and modern web technologies**