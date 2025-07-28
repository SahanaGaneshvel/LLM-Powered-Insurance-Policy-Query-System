# ✅ Vercel Deployment Checklist

## 📋 Pre-Deployment Checklist

### 1. Files Created ✅
- [x] `vercel.json` - Vercel configuration
- [x] `runtime.txt` - Python version specification
- [x] `api/index.py` - Serverless function entry point
- [x] `.gitignore` - Git ignore rules
- [x] `DEPLOYMENT.md` - Deployment guide
- [x] `test_vercel.py` - Deployment test script

### 2. Environment Variables Required
- [ ] `GROQ_API_KEY` - Your Groq API key
- [ ] `PINECONE_API_KEY` - Your Pinecone API key  
- [ ] `PINECONE_ENVIRONMENT` - Your Pinecone environment
- [ ] `API_KEY` - Authentication key for your API
- [ ] `WEBHOOK_TIMEOUT` - Timeout setting (default: 30)
- [ ] `MAX_CHUNK_SIZE` - Document chunk size (default: 1000)
- [ ] `TOP_K_RESULTS` - Number of results (default: 5)
- [ ] `BATCH_SIZE` - Batch processing size (default: 10)
- [ ] `CACHE_TTL` - Cache timeout (default: 3600)

### 3. API Keys Setup
- [ ] **Groq API Key**: [Get it here](https://console.groq.com/)
- [ ] **Pinecone API Key**: [Get it here](https://www.pinecone.io/)

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository
```bash
# Add all files to git
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### Step 2: Deploy to Vercel

**Option A: Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

**Option B: GitHub Integration**
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure environment variables
5. Deploy

### Step 3: Configure Environment Variables
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add all required environment variables (see list above)

### Step 4: Test Your Deployment
```bash
# Health check
curl https://your-project.vercel.app/health

# Test API endpoint
curl -X POST https://your-project.vercel.app/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "documents": "https://example.com/policy.pdf",
    "questions": ["What is the grace period?"]
  }'
```

## 🔍 Post-Deployment Verification

### 1. Check Endpoints
- [ ] `/health` - Health check endpoint
- [ ] `/docs` - API documentation
- [ ] `/hackrx/run` - Main API endpoint

### 2. Test Functionality
- [ ] Health check returns 200 OK
- [ ] API documentation loads correctly
- [ ] Main endpoint accepts requests
- [ ] Authentication works properly

### 3. Monitor Performance
- [ ] Check Vercel function logs
- [ ] Monitor response times
- [ ] Verify error handling

## ⚠️ Important Notes

### Serverless Limitations
- **Timeout**: 10-second limit on free tier
- **Memory**: Limited memory allocation
- **Cold Starts**: First request may be slower
- **File Size**: Document size limitations

### Performance Optimization
- Use smaller document chunks for faster processing
- Implement caching for repeated requests
- Consider background processing for large documents
- Monitor and optimize API calls

### Security
- Never commit API keys to repository
- Use Vercel's environment variable management
- Enable HTTPS in production
- Implement proper authentication

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Environment Variable Issues**
   - Verify all variables are set in Vercel dashboard
   - Check variable names match your code

3. **Timeout Errors**
   - Optimize code for faster execution
   - Break large operations into smaller chunks

4. **Memory Issues**
   - Reduce document chunk sizes
   - Implement streaming for large files

### Debug Commands
```bash
# Test local setup
python test_vercel.py

# Check imports
python -c "from app import app; print('App imported successfully')"

# Test API entry point
python -c "from api.index import handler; print('Handler imported successfully')"
```

## 📊 Monitoring

### Vercel Dashboard
- Function execution logs
- Performance metrics
- Error tracking
- Deployment status

### Health Checks
- Regular endpoint testing
- Response time monitoring
- Error rate tracking

## 🔄 Updates

### Updating Deployment
1. Make changes to your code
2. Commit and push to repository
3. Vercel will automatically redeploy

### Rollback
- Use Vercel dashboard to rollback to previous deployment
- Check function logs for issues

---

**🎉 Ready for Deployment!**

Your project is now configured for Vercel deployment. Follow the checklist above to complete the deployment process. 