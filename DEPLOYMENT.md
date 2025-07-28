# 🚀 Vercel Deployment Guide

This guide will help you deploy your LLM-Powered Insurance Policy Query System to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub/GitLab Account**: For repository hosting
3. **API Keys**: Ensure you have the required API keys (see Configuration section)

## 🔧 Configuration

### 1. Environment Variables

Before deploying, you need to set up your environment variables in Vercel:

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following variables:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
API_KEY=your_api_key_for_authentication
WEBHOOK_TIMEOUT=30
MAX_CHUNK_SIZE=1000
TOP_K_RESULTS=5
BATCH_SIZE=10
CACHE_TTL=3600
```

### 2. API Keys Required

- **Groq API Key**: [Get it here](https://console.groq.com/)
- **Pinecone API Key**: [Get it here](https://www.pinecone.io/)

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

### Option 2: Deploy via GitHub Integration

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure environment variables
   - Deploy

### Option 3: Deploy via Vercel Dashboard

1. **Upload Project**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Upload your project files
   - Configure environment variables
   - Deploy

## 🔍 Post-Deployment

### 1. Verify Deployment

After deployment, your API will be available at:
- **Main API**: `https://your-project.vercel.app/hackrx/run`
- **Health Check**: `https://your-project.vercel.app/health`
- **Documentation**: `https://your-project.vercel.app/docs`

### 2. Test Your API

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

## ⚠️ Important Notes

### 1. Serverless Limitations

- **Cold Starts**: First request may be slower
- **Timeout**: 10-second timeout limit on Vercel's free tier
- **Memory**: Limited memory allocation
- **File Size**: Document size limitations

### 2. Performance Optimization

- **Caching**: Use Redis or similar for caching
- **Async Processing**: Consider background jobs for large documents
- **Chunking**: Process documents in smaller chunks

### 3. Environment Variables

- **Security**: Never commit API keys to your repository
- **Production**: Use Vercel's environment variable management
- **Validation**: Ensure all required variables are set

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Environment Variable Issues**
   - Verify all variables are set in Vercel dashboard
   - Check variable names match your code

3. **Timeout Errors**
   - Optimize your code for faster execution
   - Consider breaking large operations into smaller chunks

4. **Memory Issues**
   - Reduce document chunk sizes
   - Implement streaming for large files

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📊 Monitoring

### Vercel Analytics

- **Function Logs**: Check Vercel dashboard for function logs
- **Performance**: Monitor function execution times
- **Errors**: Review error logs in Vercel dashboard

### Health Checks

Regularly test your endpoints:
- `/health` - System health
- `/docs` - API documentation
- `/hackrx/run` - Main functionality

## 🔄 Updates

### Updating Your Deployment

1. **Make Changes**: Update your code
2. **Commit**: Push to your repository
3. **Deploy**: Vercel will automatically redeploy

### Rollback

If needed, you can rollback to previous deployments in the Vercel dashboard.

## 📞 Support

- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)

---

**🎉 Your API is now live on Vercel!** 