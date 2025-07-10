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
from yt_dlp import YoutubeDL

load_dotenv()
        
async def take_screenshot():
    try:
        timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"

        desktop_paths = [
            Path.home() / "Desktop",
            Path(os.environ.get("USERPROFILE", "")) / "Desktop",
            Path(os.environ.get("HOMEPATH", "")) / "Desktop",
            Path(os.environ.get("ONEDRIVE", "")) / "Desktop",
        ]
        desktop_path = next((path for path in desktop_paths if path.exists()), None)

        if not desktop_path:
            return "Could not locate Desktop folder."

        screenshots_dir = desktop_path / "Jarvis_Screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        file_path = screenshots_dir / filename

        screenshot = await asyncio.to_thread(pyautogui.screenshot)
        await asyncio.to_thread(screenshot.save, file_path)

        return f"Screenshot saved at: {file_path}"
    
    except Exception as e:
        return f"Failed to take screenshot: {e}"


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
    
async def play_song():
    song_name = input("Enter the song you want to play: ")
    try:
        await asyncio.to_thread(pywhatkit.playonyt, song_name)
        return f"Playing {song_name} on YouTube."
    except Exception as e:
        return f"Failed to play the song: {e}"
    
async def download_youtube_video():
    try:
        url = input("Enter the YouTube video URL: ").strip()

        desktop_paths = [
            Path.home() / "Desktop",
            Path(os.environ.get("USERPROFILE", "")) / "Desktop",
            Path(os.environ.get("HOMEPATH", "")) / "Desktop",
            Path(os.environ.get("ONEDRIVE", "")) / "Desktop",
        ]
        desktop_path = next((path for path in desktop_paths if path.exists()), None)

        if not desktop_path:
            return "Could not locate Desktop folder."

        download_folder = desktop_path / "Downloaded Videos"
        os.makedirs(download_folder, exist_ok=True)

        ydl_opts = {
            'outtmpl': str(download_folder / '%(title)s.%(ext)s'),
            'format': 'best'
        }

        def run_download():
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(run_download)

        return f"Video downloaded successfully to: {download_folder}"

    except Exception as e:
        return f"Failed to download video. Error: {str(e)}"
                   

async def open_downloads_folder():
    try:
        possible_paths = [
            Path.home() / "Downloads",
            Path(os.environ.get("USERPROFILE", "")) / "Downloads",
            Path(os.environ.get("HOMEPATH", "")) / "Downloads",
            Path(os.environ.get("ONEDRIVE", "")) / "Downloads",
        ]

        downloads_path = next((p for p in possible_paths if p.exists()), None)

        if not downloads_path:
            return "Could not locate Downloads folder."

        await asyncio.to_thread(subprocess.Popen, ["explorer", str(downloads_path)])
        return f"Opened Downloads folder at: {downloads_path}"

    except Exception as e:
        return f"Failed to open Downloads folder: {e}"
        
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

