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
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)

knowledgeBase = ""

def getHeadlines():
    global knowledgeBase
    headlines = []
    session = HTMLSession()
    url = "https://www.livemint.com/"
    req = session.get(url)
    articles = req.html.find('h3 a')
    newslist = []
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
                    content = summary[0]['summary_text']
                    knowledgeBase += title.text + "\n" + content + "\n\n"
                    print("----"*100)
                    print(content)
                    newslist.append({"title":title.text,"body": content})
                    cnt += 1
            if cnt == 3:
                break
        except:
            pass
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
