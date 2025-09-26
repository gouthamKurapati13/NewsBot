from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelWithLMHead
from transformers import pipeline
from requests_html import HTMLSession
import warnings

# engine = pyttsx3.init()
warnings.filterwarnings('ignore') 

app = Flask(__name__)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelWithLMHead.from_pretrained(model_name)

knowledgeBase = ""

def getHeadlines():
    global knowledgeBase
    headlines = []
    session = HTMLSession()
    url = "https://www.livemint.com/"
    req = session.get(url)
    
    # Try multiple selectors for articles
    articles = req.html.find('h3 a')
    if not articles:
        articles = req.html.find('h2 a')
    if not articles:
        articles = req.html.find('h1 a')
    if not articles:
        articles = req.html.find('a[href*="/news/"]')
    
    newslist = []
    cnt = 0
    
    for article in articles[:10]:  # Limit to first 10 articles
        try:
            links = list(article.absolute_links)
            if not links:
                continue
                
            article_url = links[0]
            article_req = session.get(article_url)
            
            # Try multiple selectors for title
            title = article_req.html.find('#article-0', first=True)
            if not title:
                title = article_req.html.find('h1', first=True)
            if not title:
                title = article_req.html.find('.headline', first=True)
            
            # Try multiple selectors for content
            content = article_req.html.find('.storyPage_storyContent__m_MYl', first=True)
            if not content:
                content = article_req.html.find('.story-content', first=True)
            if not content:
                content = article_req.html.find('.article-content', first=True)
            if not content:
                # Get all paragraphs as fallback
                paragraphs = article_req.html.find('p')
                if paragraphs and len(paragraphs) > 2:
                    content_text = ' '.join([p.text for p in paragraphs[:5] if p.text.strip()])
                    if len(content_text) > 100:  # Only if we have substantial content
                        content = type('obj', (object,), {'text': content_text})
            
            if title and content and hasattr(content, 'text') and len(content.text.strip()) > 50:
                # Limit content length for summarization
                content_text = content.text[:2000]  # Limit to prevent memory issues
                word_count = len(content_text.split())
                max_length = min(150, max(50, word_count // 4))  # Dynamic max length
                
                summary = summarizer(content_text, max_length=max_length, min_length=30, do_sample=False)
                if summary:
                    summary_text = summary[0]['summary_text']
                    knowledgeBase += title.text + "\n" + summary_text + "\n\n"
                    newslist.append({"title": title.text, "body": summary_text})
                    cnt += 1
                    
            if cnt >= 3:  # Stop after getting 3 good articles
                break
                
        except Exception as e:
            continue
    
    return newslist

def getSportsNews():
    global knowledgeBase
    sports_news = []
    session = HTMLSession()
    url = "https://www.livemint.com/sports"
    req = session.get(url)
    articles = req.html.find('h2 a')
    cnt = 0
    for article in articles:
        links = list(article.absolute_links)
        req = session.get(links[0])
        title = req.html.find('#article-0', first=True)
        content = req.html.find('.storyPage_storyContent__m_MYl', first=True)
        try:
            if title and content:
                summary = summarizer(content.text, max_length=content.text.count(" "), do_sample=False)
                if summary:
                    sports_news.append({"title": title.text, "body": summary[0]['summary_text']})
                    knowledgeBase += title.text + "\n" + summary[0]['summary_text'] + "\n\n"
                    cnt += 1
            if cnt == 2:
                break
        except:
            pass
    print(sports_news)
    return sports_news

def getStockValues():
    global knowledgeBase
    stock_values = {"gainers": [], "losers": []}
    session = HTMLSession()
    url = "https://www.livemint.com/market/stock-market-news"
    req = session.get(url)
    
    gainers = req.html.find('.lhsgainerloser.BSE.gainer')
    losers = req.html.find('.lhsgainerloser.BSE.loser')
    
    for gainer in gainers:
        name = gainer.find('li', first=True).text
        price = gainer.find('li span.up', first=True).text
        stock_values["gainers"].append({"name": name, "price": price})
        knowledgeBase += name + " - Price: " + price + "\n"
    
    for loser in losers:
        name = loser.find('li', first=True).text
        price = loser.find('li span.down', first=True).text
        stock_values["losers"].append({"name": name, "price": price})
        knowledgeBase += name + " - Price: " + price + "\n"
    
    print(stock_values)
    return stock_values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def answer_question():
    global knowledgeBase
    data = request.get_json()
    question = data['question']
    print(question)
    if question == "Headlines":
        print("Getting headlines")
        hl = getHeadlines()
        print(hl)
        return jsonify({'answer': hl})
    # Removed handling for CATEGORY and TOPIC
    elif "yes" in question.lower():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        news = ""
        for headline in hl:
            news += headline["title"] + "\n" + headline["body"] + "\n\n"
        engine.setProperty('voice', voices[0].id)
        engine.say(news)
        engine.runAndWait()
        engine.stop()
        if engine._inLoop:
            engine.endLoop()
        return jsonify({'answer': "That is the end of the podcast so far."})
    else:
        input_text = "question: {} context: {}".format(question, knowledgeBase)
        encoded_input = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True)
        output = model.generate(input_ids=encoded_input.input_ids, attention_mask=encoded_input.attention_mask)
        print(knowledgeBase)
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        if answer:
            return jsonify({'answer': answer})
        else:
            return jsonify({'answer': "Sorry, I don't understand what you're asking about."})

@app.route('/discuss', methods=['POST'])
def discuss():
    global knowledgeBase
    data = request.get_json()
    question = data['question']
    input_text = "question: {} context: {}".format(question, knowledgeBase)
    encoded_input = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True)
    output = model.generate(input_ids=encoded_input.input_ids, attention_mask=encoded_input.attention_mask)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    if answer:
        return jsonify({'answer': answer})
    else:
        return jsonify({'answer': "Sorry, I don't understand what you're asking about."})

@app.route('/sports', methods=['GET'])
def sports_news():
    sports_news = getSportsNews()
    return jsonify({'answer': sports_news})

@app.route('/stocks', methods=['GET'])
def stocks():
    stock_values = getStockValues()
    return jsonify({'answer': stock_values})

if __name__ == '__main__':
    app.run(debug=True)
