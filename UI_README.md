# 🏥 Insurance Policy Query System - Web UI

A beautiful, modern web interface for the LLM-Powered Insurance Policy Query System.

## 🚀 Quick Start

### Option 1: Start UI Server
```bash
python start_ui.py
```

### Option 2: Direct Server Start
```bash
python ui_server.py
```

### Option 3: Manual Start
```bash
uvicorn ui_server:app --host 0.0.0.0 --port 8080 --reload
```

## 📱 Access the UI

Once the server is running, open your browser and go to:
- **Main UI**: http://localhost:8080
- **API Endpoint**: http://localhost:8080/hackrx/run
- **Health Check**: http://localhost:8080/health

## 🎯 Features

### ✨ Modern Interface
- **Clean Design**: Beautiful gradient background and modern UI
- **Responsive**: Works on desktop, tablet, and mobile
- **User-Friendly**: Intuitive form with dynamic question management

### 🔧 Functionality
- **Document URL Input**: Paste any PDF/DOCX document URL
- **Dynamic Questions**: Add/remove questions as needed
- **Sample Questions**: Quick load button for testing
- **Real-time Processing**: Live status updates during processing
- **Results Display**: Clean, organized answer presentation

### 🛡️ Security
- **Bearer Token Authentication**: Secure API access
- **Input Validation**: Proper error handling and validation
- **CORS Support**: Cross-origin request handling

## 📋 How to Use

### 1. Enter Document URL
- Paste the URL of your insurance policy document
- Supports PDF, DOCX, and email formats
- Default URL is pre-filled for testing

### 2. Add Questions
- Type your questions in the input fields
- Click "+ Add Question" to add more
- Click "Remove" to delete questions
- Use "📋 Load Sample Questions" for quick testing

### 3. Process Questions
- Click "🚀 Process Questions" to start
- Watch the loading spinner
- Results appear automatically when complete

### 4. View Results
- Questions and answers are clearly displayed
- Each result shows the question and detailed answer
- Scroll to see all results

## 🔧 API Integration

The UI connects to your existing API endpoints:

### Main Endpoint
```
POST /hackrx/run
Content-Type: application/json
Authorization: Bearer 4a7809a665f2f39b1f2fa7c7073518e6baa4ebe9309eea30dae92adba5772d8c

{
    "documents": "https://example.com/policy.pdf",
    "questions": [
        "What is the grace period?",
        "What is covered under maternity?"
    ]
}
```

### Response Format
```json
{
    "answers": [
        "A grace period of thirty days is provided...",
        "Yes, the policy covers maternity expenses..."
    ]
}
```

## 🎨 UI Features

### Design Elements
- **Gradient Background**: Beautiful purple-blue gradient
- **Card Layout**: Clean white cards with shadows
- **Color Coding**: Green for success, red for errors
- **Icons**: Emoji icons for better visual appeal
- **Animations**: Smooth hover effects and transitions

### Interactive Elements
- **Dynamic Forms**: Add/remove questions on the fly
- **Loading States**: Spinner animation during processing
- **Error Handling**: Clear error messages
- **Success Feedback**: Positive confirmation messages

## 📊 Sample Questions

The UI includes 10 sample questions for testing:

1. "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
2. "What is the waiting period for pre-existing diseases (PED) to be covered?"
3. "Does this policy cover maternity expenses, and what are the conditions?"
4. "What is the waiting period for cataract surgery?"
5. "Are the medical expenses for an organ donor covered under this policy?"
6. "What is the No Claim Discount (NCD) offered in this policy?"
7. "Is there a benefit for preventive health check-ups?"
8. "How does the policy define a 'Hospital'?"
9. "What is the extent of coverage for AYUSH treatments?"
10. "Are there any sub-limits on room rent and ICU charges for Plan A?"

## 🔄 Demo Mode

The UI includes a demo mode that shows mock responses when the API is not available:

- **Mock Responses**: Pre-defined accurate answers
- **Realistic Timing**: 2-second processing simulation
- **Error Handling**: Graceful fallback for API errors

## 🛠️ Technical Details

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Vanilla JS for interactivity
- **Responsive Design**: Mobile-first approach

### Backend
- **FastAPI**: High-performance Python web framework
- **CORS**: Cross-origin resource sharing enabled
- **Static Files**: Serves HTML directly
- **Authentication**: Bearer token validation

### Integration
- **Document Parser**: Processes PDF/DOCX files
- **Embedding Service**: Vector search capabilities
- **Groq Service**: LLM-powered answer generation
- **Performance Monitoring**: Request timing and statistics

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the UI server
python start_ui.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn ui_server:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t insurance-ui .
docker run -p 8080:8080 insurance-ui
```

## 📝 File Structure

```
├── ui.html              # Main UI interface
├── ui_server.py         # FastAPI server
├── start_ui.py          # Startup script
├── UI_README.md         # This file
└── [existing files]     # Your existing system files
```

## 🎯 Benefits

### For Users
- **Easy to Use**: No technical knowledge required
- **Visual Feedback**: Clear loading and success states
- **Flexible**: Add/remove questions as needed
- **Fast**: Quick processing and response times

### For Developers
- **Clean Code**: Well-organized HTML/CSS/JS
- **Modular**: Easy to extend and customize
- **Responsive**: Works on all devices
- **Accessible**: Proper semantic markup

## 🔮 Future Enhancements

- **File Upload**: Direct file upload instead of URLs
- **Export Results**: Download results as PDF/CSV
- **Question Templates**: Pre-built question sets
- **Multi-language**: Support for different languages
- **Dark Mode**: Toggle between light/dark themes
- **Advanced Analytics**: Processing time and accuracy metrics

---

**🎉 Your Insurance Policy Query System now has a beautiful, professional web interface!** 