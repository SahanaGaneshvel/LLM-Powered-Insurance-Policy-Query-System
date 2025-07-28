# 🏥 LLM-Powered Insurance Policy Query System

An intelligent document analysis and question-answering system designed for insurance policy queries. This system processes PDFs, DOCX, and email documents, retrieves relevant clauses using embeddings, and generates accurate answers using LLM reasoning.

## ✨ Features

### 🎯 Core Capabilities
- **Document Processing**: Supports PDF, DOCX, and email documents
- **Intelligent Retrieval**: Uses embeddings for semantic search
- **LLM-Powered Answers**: Generates detailed, accurate responses
- **Fast Performance**: Optimized for 2-3 second response times
- **Web Interface**: Beautiful, user-friendly UI
- **Webhook Integration**: Asynchronous result submission

### 🎨 User Interface
- **Modern Design**: Clean, professional web interface
- **Dynamic Forms**: Add/remove questions easily
- **Sample Questions**: Quick-load predefined questions
- **Real-time Feedback**: Loading indicators and error handling
- **Responsive Layout**: Works on desktop and mobile

### 🔧 Technical Features
- **Modular Architecture**: Separated into distinct components
- **Vector Search**: Pinecone integration for fast similarity search
- **Caching System**: In-memory and optional Redis caching
- **Performance Monitoring**: Request tracking and optimization
- **Security**: Bearer token authentication
- **Error Handling**: Robust error management and logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required API keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LLM-Powered-Insurance-Policy-Query-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your API keys
   ```

4. **Start the system**

   **Option A: Web UI (Recommended)**
   ```bash
   python start_ui.py
   ```
   Then open: http://localhost:8080

   **Option B: API Server**
   ```bash
   python start.py
   ```
   API endpoint: http://localhost:8000/hackrx/run

## 🎯 Usage

### Web Interface (Recommended)

1. **Open the UI**: Navigate to http://localhost:8080
2. **Enter Document URL**: Paste your policy document URL
3. **Add Questions**: Use the dynamic form to add your questions
4. **Load Sample Questions**: Click "📋 Load Sample Questions" for predefined queries
5. **Process**: Click "🚀 Process Questions" to get answers
6. **View Results**: See detailed Q&A format results

### API Usage

**Endpoint**: `POST /hackrx/run`

**Request Format**:
```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

**Response Format**:
```json
{
  "answers": [
    "A grace period of thirty days is provided...",
    "There is a waiting period of thirty-six months..."
  ]
}
```

**Authentication**: Bearer token required in headers

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Keys
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# Authentication
API_KEY=your_api_key_for_authentication

# Performance Settings
WEBHOOK_TIMEOUT=30
MAX_CHUNK_SIZE=1000
TOP_K_RESULTS=5
BATCH_SIZE=10
CACHE_TTL=3600

# Optional: Redis Cache
REDIS_URL=redis://localhost:6379
```

### API Keys Required

1. **Groq API Key**: For LLM operations
   - Sign up at: https://console.groq.com/
   - Used for query parsing and answer generation

2. **Pinecone API Key**: For vector database
   - Sign up at: https://www.pinecone.io/
   - Used for embedding storage and similarity search

## 🏗️ Architecture

### Core Components

```
├── app.py                 # Main FastAPI application
├── ui_server.py          # Web UI server
├── api_routes.py         # API endpoint definitions
├── document_parser.py    # Document processing
├── embedding_service.py  # Embedding and vector search
├── groq_service.py      # LLM operations
├── utils.py             # Utilities and helpers
└── ui.html              # Web interface
```

### Data Flow

1. **Document Processing**: PDF/DOCX parsing and text extraction
2. **Embedding Generation**: Convert text chunks to vectors
3. **Vector Storage**: Store in Pinecone for similarity search
4. **Query Processing**: Parse user questions
5. **Retrieval**: Find relevant document chunks
6. **Answer Generation**: Use LLM to generate detailed answers
7. **Response**: Return structured JSON with answers

## 📊 Performance Optimization

### Latency Targets
- **Total Response Time**: 2-3 seconds
- **Document Processing**: < 1 second
- **Embedding Generation**: < 0.5 seconds
- **Vector Search**: < 0.3 seconds
- **LLM Generation**: < 1.5 seconds

### Optimization Features
- **Batch Processing**: Parallel embedding generation
- **Caching**: In-memory and Redis caching
- **Chunking**: Optimal text chunk sizes
- **Async Operations**: Non-blocking I/O
- **Connection Pooling**: Efficient API calls

## 🔒 Security

### Authentication
- **Bearer Token**: Required for API access
- **Environment Variables**: Secure key storage
- **Input Validation**: Request sanitization

### Data Protection
- **No Data Storage**: Documents processed in memory
- **Secure APIs**: HTTPS recommended for production
- **Error Handling**: No sensitive data in logs

## 🧪 Testing

### Quick Test
```bash
python test_system.py
```

### Manual Testing
1. Start the UI server: `python start_ui.py`
2. Open http://localhost:8080
3. Use sample questions or add your own
4. Verify responses are accurate and detailed

## 🐛 Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**2. API Key Errors**
- Verify your `.env` file has correct keys
- Check API key permissions and quotas

**3. Pinecone Connection Issues**
- Verify environment and API key
- Check index name and configuration

**4. Performance Issues**
- Monitor system resources
- Check network connectivity
- Verify API rate limits

### Debug Mode
```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
python start_ui.py
```

## 📈 Monitoring

### Health Checks
- **UI Health**: http://localhost:8080/health
- **API Health**: http://localhost:8000/health
- **Stats**: http://localhost:8080/api/v1/stats

### Performance Metrics
- Request processing times
- Error rates and types
- Cache hit rates
- API response times

## 🔄 Updates and Maintenance

### Regular Maintenance
- Monitor API quotas and usage
- Update dependencies regularly
- Review and optimize performance
- Backup configuration files

### Scaling Considerations
- Load balancing for multiple instances
- Database scaling for high volume
- CDN for document delivery
- Monitoring and alerting setup

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs for error details
- Verify configuration and API keys
- Test with sample data first

---

**🎉 Ready to use!** Start with the web UI for the best experience. 