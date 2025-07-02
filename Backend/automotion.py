from intent_classifier import predict_intent
import os
from dotenv import load_dotenv
import pywhatkit
import datetime as dt
import subprocess
import pyautogui
import time
import requests
import json
import random

load_dotenv()


    
def tell_jokes():
    response = requests.get("https://official-joke-api.appspot.com/jokes/random")
    if response.status_code == 200:
        joke = response.json()
        return f"{joke['setup']} ... {joke['punchline']}"
    else:
        return "Sorry, I couldn't fetch a joke right now."
def getting_news():
    url = f"https://newsapi.org/v2/everything?q=india-pakistan&apiKey={os.getenv('newsapi')}" 
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        headlines = [article['title'] for article in articles[:5]]
        return "\n".join(headlines)
    else:
        return "Sorry, I couldn't fetch the news right now."

def get_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['text']
    return "Couldn't fetch a fact right now!"

def get_quotes():
    response = requests.get("https://zenquotes.io/api/random")
    if response.ok:
        quote_data = response.json()[0]
        return f"\"{quote_data['q']}\" — {quote_data['a']}"
    return "Couldn't fetch a quote right now."

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

# if __name__ == "__main__":
#     load_dotenv()
#     while True:
#         query = input("User: ")
#         if query == 'quit':
#             break
#         intent = predict_intent(query)
#         print(intent)
#         if intent == 'tell_joke':
#             print(f"Jarvis: {tell_jokes()}")
#         elif intent == 'get_news':
#             print(f"Jarvis: {getting_news()}")
#         elif intent == 'get_fact':
#             print(f"Jarvis: {get_random_fact()}")
#         elif intent == 'get_quote':
#             print(f"Jarvis: {get_quotes()}")
#         elif intent == 'get_weather':
#             print(f"Jarvis: {weather_update()}")

