from transformers import pipeline, AutoTokenizer, AutoModelWithLMHead
from requests_html import HTMLSession

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# session = HTMLSession()
# url = "https://www.livemint.com/"
# req = session.get(url)
# articles = req.html.find('h3 a')

# cnt = 0
# for article in articles:
#     links = list(article.absolute_links)
#     req = session.get(links[0])
#     title = req.html.find('#article-0', first=True)
#     content = req.html.find('.storyPage_storyContent__m_MYl', first=True)
#     try:
#       if title and content:
#         summary = summarizer(content.text, max_length=content.text.count(" "), do_sample=False)
#         if summary:
#           print(title.text)
#           print(summary[0]['summary_text'])
#           print("-----"*30)
#           cnt += 1
#       if cnt == 5:
#         break
#     except:
#       pass

def test_discuss(question):
    model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelWithLMHead.from_pretrained(model_name)
    
    knowledgeBase = """In a landmark development for sustainable energy, scientists at the GreenTech Institute have unveiled a revolutionary solar panel capable of converting sunlight into electricity with an efficiency of 50%—nearly double the current industry standard. The breakthrough, achieved through advanced nanotechnology and quantum dot research, is expected to significantly reduce the cost of solar power and make it more accessible worldwide."""
    # headlines = getHeadlines()
    # for headline in headlines:
    #     knowledgeBase += headline["title"] + "\n" + headline["body"] + "\n\n"
    
    input_text = "question: {} context: {}".format(question, knowledgeBase)
    encoded_input = tokenizer(input_text, return_tensors='pt', max_length=512, truncation=True)
    output = model.generate(input_ids=encoded_input.input_ids, attention_mask=encoded_input.attention_mask)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

# Example usage:
if __name__ == "__main__":
    question = "What are the latest headlines?"
    print(test_discuss(question))


