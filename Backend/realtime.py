from groq import Groq
import os
import time
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import requests
from .intent_classifier import predict_intent
from bs4 import BeautifulSoup
import datetime as dt
import yfinance as yf
import spacy
load_dotenv()
Username = os.getenv('User')
Assistantname = os.getenv('Assistantname')
client = Groq(api_key=os.getenv('GroqAPI'))
day = dt.datetime.now().day
month = dt.datetime.now().strftime("%B")
year = dt.datetime.now().year


def getting_news_topic(query):
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE", "PERSON", "NORP", "EVENT", "WORK_OF_ART"]:
            return ent.text
    return query

def getting_news(query):
    topic = getting_news_topic(query)
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={os.getenv('newsapi')}" 
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        headlines = [article['title'] for article in articles[:5]]
        description = [article['description'] for article in articles[:5]]
        headlines = [f"Title: {title}\nDescription: {desc}" for title, desc in zip(headlines, description)]
        return "\n".join(headlines)
    else:
        return "Sorry, I couldn't fetch the news right now."
    
def weather_update():
    city = "Puruliya"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('WEATHER_API')}&units=metric"
    response = requests.get(weather_url)
    data = response.json()
    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return f"Sir, the weather at {city} is currently {weather}. The temperature is {temperature} degrees Celsius with a humidity level of {humidity} percent. Wind speed is {wind_speed} meters per second."
    else:
        return "Error fetching weather data."
def extract_company_name(query):
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            return ent.text
    return query 
def search_yahoo_finance(query):
    company = extract_company_name(query)
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        
        if res.status_code != 200:
            return None, "API request failed"

        data = res.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            best = data['quotes'][0]
            symbol = best.get('symbol')
            return symbol
        else:
            return None, "No quotes found"

    except Exception as e:
        return None, "Exception occurred"
def get_global_stock_yahoo(query):
    ticker = search_yahoo_finance(query)
    if ticker is None:
        return "Ticker not found"
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    latest_price = data["Close"].iloc[-1]
    return f"${latest_price}"

def YepSearch(query, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))

            if not results:
                return f"No search results found for '{query}'."

            answer = f"The search results for '{query}' are:\n[start]\n"
            for i in results:
                answer += f"Title: {i['title']}\nSnippet: {i['body']}\nURL: {i['href']}\n\n"
            answer += "[end]"
            return answer

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
            attempt += 1

    return f"Search failed for '{query}' after {retries} attempts."

def modifyAnswer(answer):
    lines = answer.split('\n')
    non_empty_line = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_line)
    return modified_answer

def getGroqResponse(user_query, raw_search_results):
    Username = os.getenv('User')
    Assistantname = os.getenv('Assistantname')
    client = Groq(api_key=os.getenv('GroqAPI'))
    day = dt.datetime.now().day
    month = dt.datetime.now().strftime("%B")
    year = dt.datetime.now().year
    System = f"""Hello, I am {Username}, You call me 'Sir', You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
    *** Today's date is {day} {month} of {year}.***
    *** Always remember I am an Indian.***
    *** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
    *** Just answer the question from the provided data in a professional way. ***
    *** Please read the whole thing and always give to the point answer. ***"""
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": System},
            {"role": "user", "content": f"Query: {user_query}\n\n{raw_search_results}"}
        ]
    )
    return chat_completion.choices[0].message.content

def get_groq_response(query, prompt, raw_search_results):
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Query: {query}\n\n{raw_search_results}"}
        ]
    )
    return chat_completion.choices[0].message.content

def main(query):
    intent = predict_intent(query)
    if intent == 'get_news':
        news = getting_news(query)
        prompt = f"Hello, You are a news assistant. Your job is to tell the news in a prefessional way. The news has a headline and a description. Please read the whole thing and always give to the point answer. There are 5 news articles. Please provide the news in a professional way."
        return get_groq_response(query, prompt, news)
    elif intent == 'get_weather':
        return weather_update()
    elif 'stock' in query or 'share' in query:
        return f"The current stock price of {extract_company_name(query)} is {get_global_stock_yahoo(query)}"
    else:
        ans = YepSearch(query)
        m_ans = modifyAnswer(ans)
        return getGroqResponse(query, m_ans)
# while True:
#     query = input("User: ")
#     if query == 'quit':
#         break
#     answer = main(query)
#     print(f"{Assistantname}: {answer}")
