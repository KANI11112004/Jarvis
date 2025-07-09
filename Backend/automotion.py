#from intent_classifier import predict_intent
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
import webbrowser
import sys
from pathlib import Path
import asyncio

load_dotenv()
    
async def tell_jokes():
    def fetch_joke():
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            joke = response.json()
            return f"{joke['setup']} ... {joke['punchline']}"
        else:
            return "Sorry, I couldn't fetch a joke right now."

    return await asyncio.to_thread(fetch_joke)

async def getting_news():
    def fetch_news():
        url = f"https://newsapi.org/v2/everything?q=india-pakistan&apiKey={os.getenv('newsapi')}" 
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data['articles']
            headlines = [article['title'] for article in articles[:5]]
            return "\n".join(headlines)
        else:
            return "Sorry, I couldn't fetch the news right now."
        
    return await asyncio.to_thread(fetch_news)    

async def get_random_fact():
    def fetch_fact():
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['text']
        return "Couldn't fetch a fact right now!"
    return await asyncio.to_thread(fetch_fact)

async def get_quotes():
    def fetch_quote():
        response = requests.get("https://zenquotes.io/api/random")
        if response.ok:
            quote_data = response.json()[0]
            return f"\"{quote_data['q']}\" — {quote_data['a']}"
        return "Couldn't fetch a quote right now."
    return await asyncio.to_thread(fetch_quote)

async def weather_update():
    def fetch_weather():
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
    return await asyncio.to_thread(fetch_weather)    
    
async def take_screenshot():
    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    screenshot = await asyncio.to_thread(pyautogui.screenshot)
    await asyncio.to_thread(screenshot.save,filename)
    return f"Screenshot saved as {filename}"  

async def open_thing(query):
    query = query.lower()
    
    websites = {
        "youtube" : "https://www.youtube.com",
        "gmail" : "https://mail.google.com",
        "google" : "https://www.google.com",
        "github": "https://github.com",
        "stackoverflow" : "https://stackoverflow.com"
    }  
    
    apps = {
        "notepad" : "notepad" if sys.platform.startswith("win") else "gedit",
        "calculator" : "calc" if sys.platform.startswith("win") else "gnome-calculator",
        "vscode" : "code"
    }
    
    for site in websites:
        if site in query:
            await asyncio.to_thread(webbrowser.open,websites[site])
            return f"Opening {site} in your browser."
        
    for app in apps:
        if app in query:
            try:
                await asyncio.to_thread(subprocess.Popen,apps[app])
                return f"Opening {app}."
            except Exception as e:
                return f"Failed to open {app}: {str(e)}"
    return "Sorry, I could not find what to open."  

async def send_whatsapp_message():
    number = input("Enter the phone number with counrty code: ")
    
    message = input("What should I send?\t")
    
    now = dt.datetime.now()
    hour = now.hour
    minute = now.minute + 2
    
    try:
        await asyncio.to_thread(pywhatkit.sendwhatmsg,number,message,hour,minute)
        return f"Scheduled your message at {hour}:{minute}. Don't close the browser until it is sent."
    except Exception as e:
        return f"Failed to send message: {str(e)}"        

async def create_folder():
    try:
        desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
        if not desktop.exists():
            desktop = Path.home() / "OneDrive" / "Desktop"

        folder_name = "Jarvis_Folder_" + dt.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        full_path = desktop / folder_name

        def make_folder():
            full_path.mkdir(parents=True, exist_ok=True)

        await asyncio.to_thread(make_folder)
        return f"Folder created at: {full_path}"
    
    except Exception as e:
        return f"Failed to create folder: {e}"

async def save_note(note_text: str):
    try:
        desktop_path = Path(os.environ["USERPROFILE"]) / "Desktop"
        if not desktop_path.exists():
            desktop_path = Path.home() / "OneDrive" / "Desktop"

        notes_dir = desktop_path / "Jarvis_Notes"
        
        await asyncio.to_thread(notes_dir.mkdir, exist_ok=True)

        timestamp = dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_name = f"note_{timestamp}.txt"
        file_path = notes_dir / file_name

        await asyncio.to_thread(file_path.write_text, note_text)

        return f"Note saved at: {file_path}"

    except Exception as e:
        return f"Failed to save note: {e}"

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

