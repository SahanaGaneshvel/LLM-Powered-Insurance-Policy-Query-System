# 🚀 Vercel Deployment Optimization Guide

## 🔧 Recent Optimizations Made

### 1. Requirements.txt Optimization ✅
- **Pinned versions**: All dependencies now have specific versions
- **Removed Redis**: Commented out Redis dependency (not needed for Vercel)
- **Optimized sizes**: Used compatible versions for serverless deployment

### 2. Vercel Configuration Updates ✅
- **Increased Lambda size**: Set `maxLambdaSize` to 50mb
- **Extended timeout**: Set `maxDuration` to 30 seconds
- **Better routing**: Improved API routing configuration

### 3. API Entry Point Enhancement ✅
- **Error handling**: Added fallback for import issues
- **Path management**: Better Python path handling
- **Graceful degradation**: Basic endpoints if main app fails to load

## 🚀 Redeploy with Optimizations

### Step 1: Update Your Local Files
```bash
# The optimizations are already applied to your files
# Just commit and push the changes
git add .
git commit -m "Optimize Vercel deployment - fix data size issue"
git push origin main
```

### Step 2: Redeploy to Vercel
```bash
# Deploy the optimized version
vercel --prod
```

## 🔍 Test Your Deployment

### 1. Check Basic Endpoints
```bash
# Health check
curl https://llm-powered-insurance-policy-query-system-e59j6k2ac.vercel.app/health

# Root endpoint
curl https://llm-powered-insurance-policy-query-system-e59j6k2ac.vercel.app/
```

### 2. Test API Documentation
```bash
# Open in browser
https://llm-powered-insurance-policy-query-system-e59j6k2ac.vercel.app/docs
```

## ⚠️ Important Notes

### Environment Variables
You still need to set these in your Vercel dashboard:
- `GROQ_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_ENVIRONMENT`
- `API_KEY`

### Performance Considerations
- **Cold starts**: First request may be slower due to ML model loading
- **Memory limits**: Large models may cause memory issues
- **Timeout**: 30-second limit (increased from default)

## 🐛 Troubleshooting

### If "Data is too long" persists:
1. **Check build logs** in Vercel dashboard
2. **Reduce dependencies** further if needed
3. **Use Vercel Pro** for larger deployments
4. **Consider alternative deployment** (Railway, Render, etc.)

### If imports fail:
1. **Check function logs** in Vercel dashboard
2. **Verify Python version** compatibility
3. **Test locally** with `python test_vercel.py`

## 📊 Monitoring

### Vercel Dashboard
- **Function Logs**: Check for import errors
- **Build Logs**: Monitor deployment process
- **Performance**: Track response times

### Health Checks
```bash
# Regular health checks
curl -s https://llm-powered-insurance-policy-query-system-e59j6k2ac.vercel.app/health | jq

# Test main endpoint (after setting environment variables)
curl -X POST https://llm-powered-insurance-policy-query-system-e59j6k2ac.vercel.app/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{"documents": "https://example.com/policy.pdf", "questions": ["What is the grace period?"]}'
```

## 🎯 Next Steps

1. **Set Environment Variables** in Vercel dashboard
2. **Test the deployment** with the URLs above
3. **Monitor performance** and adjust as needed
4. **Scale up** if needed (Vercel Pro for larger deployments)

---

**🎉 Your optimized deployment should now work!** 