# 🤖 NewsBot - AI-Powered News Assistant

A modern, responsive web application that provides real-time news updates, sports information, and stock market insights using AI-powered summarization and natural language processing.

![NewsBot Interface](static/Images/robot1.png)

## ✨ Features

### 📰 **News Services**
- **Latest Headlines** - Get top news stories from LiveMint with AI-powered summaries
- **Sports News** - Stay updated with the latest sports developments
- **Stock Market Data** - Real-time stock gainers and losers information
- **Interactive Chat** - Ask questions about the news content using AI

### 🎨 **Modern UI/UX**
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Glass Morphism** - Modern design with backdrop blur effects and gradients
- **Real-time Chat Interface** - WhatsApp-style messaging experience
- **Typing Indicators** - Visual feedback during AI processing
- **Mobile-Optimized** - Compact 2x2 button layout on mobile devices

### 🧠 **AI-Powered Features**
- **Text Summarization** - Uses Facebook's BART model for news summarization
- **Question Answering** - T5-based model for answering questions about news content
- **Smart Content Extraction** - Multiple fallback selectors for robust web scraping
- **Dynamic Length Summarization** - Adapts summary length based on content

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gouthamKurapati13/NewsBot.git
   cd NewsBot
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv newsbot_env
   source newsbot_env/bin/activate  # On Windows: newsbot_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
NewsBot/
├── app.py                 # Main Flask application
├── main.py               # Testing and development script
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── static/              # Static assets
│   └── Images/          # Application images
│       ├── NewsBot Icon.jpg
│       ├── robot1.png
│       └── User Icon.jpg
└── templates/           # HTML templates
    ├── index.html       # Main application interface
    ├── style.css        # Additional CSS (legacy)
    └── script.js        # Additional JS (legacy)
```

## 🔧 Technical Stack

### **Backend**
- **Flask** - Python web framework
- **Transformers** - Hugging Face library for AI models
- **PyTorch** - Deep learning framework
- **requests-html** - Web scraping with JavaScript support
- **pyttsx3** - Text-to-speech functionality (optional)

### **AI Models**
- **facebook/bart-large-cnn** - Text summarization
- **MaRiOrOsSi/t5-base-finetuned-question-answering** - Question answering

### **Frontend**
- **HTML5** - Modern semantic markup
- **CSS3** - Advanced styling with Flexbox/Grid
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icon library
- **Inter Font** - Modern typography

## 📱 API Endpoints

### **GET /**
Main application interface

### **POST /answer**
Process user questions and return AI-generated responses
```json
Request: {"question": "Headlines"}
Response: {"answer": [{"title": "...", "body": "..."}]}
```

### **GET /sports**
Fetch latest sports news
```json
Response: {"answer": [{"title": "...", "body": "..."}]}
```

### **GET /stocks**
Get current stock market data
```json
Response: {
  "answer": {
    "gainers": [{"name": "...", "price": "..."}],
    "losers": [{"name": "...", "price": "..."}]
  }
}
```

### **POST /discuss**
Interactive discussion about news content
```json
Request: {"question": "Tell me more about the first headline"}
Response: {"answer": "..."}
```

## 🎮 Usage Guide

### **Getting Headlines**
1. Click the "📰 Headlines" button
2. The AI will fetch and summarize the latest news stories
3. Each article includes title and AI-generated summary

### **Sports Updates**
1. Click the "⚽ Sports News" button
2. View latest sports news with summaries
3. Get updates on various sports categories

### **Stock Market Data**
1. Click the "📈 Stock Values" button
2. See top gainers (🟢) and losers (🔴)
3. Real-time price information

### **Interactive Discussion**
1. Click the "💬 Discuss" button to enable chat mode
2. Ask questions about any previously shared news
3. The AI will answer based on the news content
4. Click "End Discussion" to return to main mode

### **Direct Questions**
- Type any question in the text input
- The AI will try to answer based on available news data
- Use natural language queries

## 🛠️ Configuration

### **Environment Variables**
No environment variables required for basic functionality.

### **Model Configuration**
- Summarization model: `facebook/bart-large-cnn`
- Question-answering model: `MaRiOrOsSi/t5-base-finetuned-question-answering`
- Both models are downloaded automatically on first run

### **Web Scraping Sources**
- Primary: LiveMint (livemint.com)
- Sports: LiveMint Sports section
- Stocks: LiveMint Market section

## 🔍 Troubleshooting

### **Common Issues**

**1. Empty headlines returned**
- Check internet connection
- Verify LiveMint website accessibility
- CSS selectors may have changed (automated fallbacks included)

**2. AI models taking too long to load**
- First run downloads models (~1-2GB)
- Subsequent runs are faster
- Consider using GPU for faster inference

**3. Mobile layout issues**
- Clear browser cache
- Ensure JavaScript and CSS are enabled
- Try different mobile browsers

**4. Installation errors**
- Update pip: `pip install --upgrade pip`
- Install Visual C++ Build Tools (Windows)
- Use Python 3.8-3.11 for compatibility

### **Performance Optimization**
- Use GPU acceleration if available
- Implement model caching for production
- Consider using smaller models for faster response

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add feature"`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

### **Development Guidelines**
- Follow PEP 8 for Python code
- Use semantic HTML and modern CSS
- Test on multiple devices and browsers
- Add comments for complex logic
- Update documentation for new features

## 📄 Dependencies

### **Core Requirements**
```
Flask>=2.3.0           # Web framework
transformers>=4.30.0   # AI models
torch>=2.2.0          # Deep learning
requests-html>=0.10.0  # Web scraping
```

### **Full Dependencies** (see requirements.txt)
- tokenizers, sentencepiece - Text processing
- lxml_html_clean, pyquery - HTML parsing
- tiktoken, protobuf, blobfile - Model utilities
- pyttsx3 - Text-to-speech (optional)

## 📊 Browser Support

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🔐 Privacy & Security

- No user data is collected or stored
- All processing happens locally
- No external API keys required
- Web scraping respects robots.txt
- HTTPS recommended for production

## 📈 Performance

- **Initial load**: 2-3 seconds (model loading)
- **News fetching**: 10-15 seconds (includes AI processing)
- **Question answering**: 2-5 seconds
- **Memory usage**: ~2GB (with loaded models)

## 🐛 Known Issues

- Text-to-speech feature partially implemented
- Some news sites may block automated access
- Large news articles may exceed model context limits
- Mobile keyboard may overlap input on some devices

## 🚀 Future Enhancements

- [ ] Add more news sources
- [ ] Implement user preferences
- [ ] Add dark/light theme toggle
- [ ] Real-time news updates
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Offline mode with cached content
- [ ] Push notifications for breaking news

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: [Create an issue](https://github.com/gouthamKurapati13/NewsBot/issues)
- **Email**: goutham.kurapati@example.com
- **Documentation**: This README file

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

*Last updated: September 2025*
