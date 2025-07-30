# Vercel Deployment Guide

## 🚀 Deploy to Vercel

Vercel is an excellent choice for deploying FastAPI applications with automatic scaling, global CDN, and easy environment variable management.

## Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Vercel Account** - Sign up at https://vercel.com
3. **Environment Variables** - You'll need your API keys ready

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Ensure these files are in your repository:**
   - ✅ `app.py` (main FastAPI app)
   - ✅ `vercel.json` (Vercel configuration)
   - ✅ `requirements.txt` (Python dependencies)
   - ✅ `runtime.txt` (Python version)

### Step 2: Connect to Vercel

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click "New Project"

2. **Import from GitHub**
   - Select "Import Git Repository"
   - Choose your repository
   - Click "Import"

### Step 3: Configure Project

1. **Project Settings**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

2. **Environment Variables**
   Add these in the Vercel dashboard:
   ```
   GROQ_API_KEY=your_groq_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   REDIS_URL=your_redis_url (optional)
   ```

### Step 4: Deploy

1. **Click "Deploy"**
   - Vercel will automatically build and deploy your app
   - This may take 2-5 minutes for the first deployment

2. **Wait for Build**
   - Monitor the build logs
   - The first build might take longer due to ML model downloads

## 🎯 After Deployment

### Your App URLs
- **Production**: `https://your-app-name.vercel.app`
- **API Health**: `https://your-app-name.vercel.app/health`
- **API Docs**: `https://your-app-name.vercel.app/docs`

### Test Your Deployment
1. **Health Check**: Visit `/health` endpoint
2. **API Documentation**: Visit `/docs` for interactive API docs
3. **Main Endpoint**: Test `/hackrx/run` with a POST request

## 🔧 Vercel-Specific Optimizations

### 1. Function Size Limits
Vercel has a 50MB function size limit. If you hit this:

**Solution**: Use Vercel's Edge Runtime or consider:
- Lighter ML models
- External model hosting
- Split into multiple functions

### 2. Cold Starts
ML models can cause slow cold starts:

**Solution**: 
- Use Vercel's Edge Runtime
- Implement model caching
- Consider serverless functions with longer timeouts

### 3. Environment Variables
Vercel automatically provides:
- `VERCEL_URL` - Your deployment URL
- `VERCEL_ENV` - Environment (production/preview/development)

## 🐛 Troubleshooting

### Common Issues:

1. **Build Failures**
   ```bash
   # Check build logs in Vercel dashboard
   # Common causes:
   # - Missing dependencies in requirements.txt
   # - Python version mismatch
   # - Large model files
   ```

2. **Function Timeout**
   ```json
   // In vercel.json, add:
   {
     "functions": {
       "app.py": {
         "maxDuration": 30
       }
     }
   }
   ```

3. **Memory Issues**
   - Consider using lighter models
   - Implement model caching
   - Use external model hosting

### Debug Commands:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from CLI
vercel

# Check deployment status
vercel ls
```

## 📊 Monitoring

### Vercel Analytics
- **Function Calls**: Monitor API usage
- **Response Times**: Track performance
- **Error Rates**: Identify issues

### Custom Monitoring
```python
# Add to your app.py
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 🔄 Continuous Deployment

Vercel automatically deploys when you:
- Push to `main` branch (production)
- Create pull requests (preview deployments)
- Push to other branches (preview deployments)

## 💡 Pro Tips

1. **Use Preview Deployments**
   - Test changes before production
   - Share preview URLs with team

2. **Environment-Specific Variables**
   - Set different API keys for production/preview
   - Use Vercel's environment variable management

3. **Custom Domains**
   - Add your own domain in Vercel dashboard
   - Automatic SSL certificates

4. **Performance Optimization**
   - Enable Vercel's Edge Network
   - Use CDN for static assets
   - Implement caching strategies

## 🎉 Success!

Your FastAPI application is now deployed on Vercel with:
- ✅ Global CDN
- ✅ Automatic scaling
- ✅ SSL certificates
- ✅ Custom domains
- ✅ Environment variable management
- ✅ Continuous deployment 