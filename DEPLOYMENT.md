# Deployment Guide - LLM-Powered Insurance Policy Query System

This guide provides framework presets and deployment configurations for various platforms.

## 🚀 Quick Deploy Options

### 1. Vercel (Recommended for FastAPI)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Framework Preset:** FastAPI with Python 3.9
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Serverless functions
- ✅ Environment variables support

### 2. Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway up
```

**Framework Preset:** Python FastAPI
- ✅ Automatic deployments
- ✅ Built-in PostgreSQL/Redis
- ✅ Custom domains
- ✅ Environment management

### 3. Render
```bash
# Connect your GitHub repo to Render
# Render will auto-detect the Python FastAPI framework
```

**Framework Preset:** Python Web Service
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Background workers

### 4. Heroku
```bash
# Install Heroku CLI
# Deploy using Procfile
git push heroku main
```

**Framework Preset:** Python with Procfile
- ✅ Easy deployment
- ✅ Add-ons ecosystem
- ✅ Custom domains

### 5. Docker (Any Platform)
```bash
# Build and run locally
docker-compose up -d

# Deploy to any container platform
docker build -t insurance-query-system .
docker run -p 8000:8000 insurance-query-system
```

## 🔧 Environment Variables Setup

### Required Variables
```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

### Optional Variables
```env
HOST=0.0.0.0
PORT=8000
DEBUG=false
API_KEY=your_api_key
```

## 📊 Platform Comparison

| Platform | Free Tier | Framework Preset | Auto-Deploy | Custom Domain | SSL |
|----------|-----------|------------------|-------------|---------------|-----|
| Vercel | ✅ | FastAPI | ✅ | ✅ | ✅ |
| Railway | ✅ | Python | ✅ | ✅ | ✅ |
| Render | ✅ | Python Web | ✅ | ✅ | ✅ |
| Heroku | ❌ | Python | ✅ | ✅ | ✅ |
| Docker | N/A | Custom | ❌ | ✅ | ✅ |

## 🛠️ Framework Presets Explained

### Vercel Framework Preset
- **Runtime:** Python 3.9
- **Build Command:** Automatic dependency installation
- **Start Command:** `python app.py`
- **Health Check:** `/health` endpoint
- **Features:** Serverless, edge functions, automatic scaling

### Railway Framework Preset
- **Runtime:** Python 3.9
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`
- **Health Check:** `/health` endpoint
- **Features:** Database integration, background jobs

### Render Framework Preset
- **Runtime:** Python 3.9
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`
- **Health Check:** `/health` endpoint
- **Features:** Static site hosting, background workers

## 🔍 Health Check Endpoints

All deployments include health check endpoints:
- **Main API:** `GET /health`
- **UI Server:** `GET /health` (if deployed separately)

## 📝 Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys secured
- [ ] Health check endpoint working
- [ ] CORS configured properly
- [ ] Logging set up
- [ ] Error handling implemented
- [ ] Rate limiting configured (if needed)

## 🚨 Troubleshooting

### Common Issues:
1. **Import Errors:** Ensure all dependencies in `requirements.txt`
2. **Environment Variables:** Check platform-specific env var setup
3. **Port Issues:** Verify `HOST` and `PORT` settings
4. **Memory Limits:** Consider upgrading for large models

### Platform-Specific:
- **Vercel:** Check function timeout limits
- **Railway:** Verify database connections
- **Render:** Monitor build logs
- **Heroku:** Check dyno limits

## 📚 Additional Resources

- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Vercel Python Documentation](https://vercel.com/docs/runtimes#python)
- [Railway Python Guide](https://docs.railway.app/deploy/deployments)
- [Render Python Services](https://render.com/docs/deploy-python-app) 