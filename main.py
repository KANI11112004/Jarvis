from Backend.chatbot import get_response
from Backend.realtime import main as realtime_main
# from Backend.ImageGeneration import generate_image
from Backend.model import classify_query
# from Backend.automation import perform_automation
from dotenv import load_dotenv
import os

while True:
    query = input("User: ")
    if query.lower() == 'quit':
        break

    # Classify the query
    classification = classify_query(query)

    if 'general' in classification:
        response = get_response(query)
        print(f"Jarvis: {response}")

    elif 'realtime' in classification:
        response = realtime_main(query)
        print(f"Jarvis: {response}")

    # elif 'automation' in classification:
    #     response = perform_automation(query)
    #     print(f"Jarvis: {response}")

    # elif 'image' in classification:
    #     response = generate_image(query)
    #     print(f"Jarvis: {response}")
        
    else:
        print("Jarvis: I'm not sure how to handle that query. Please try again.")
        break