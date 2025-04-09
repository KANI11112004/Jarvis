import cohere
import chatbot
from chatbot import get_response
import os
from dotenv import load_dotenv
import realtime
from realtime import YepSearch, modifyAnswer, getGroqResponse, main
load_dotenv()
co = cohere.Client(os.getenv('CohereAPI'))  # Replace with your actual API key

def classify_query(query:str):
    # Define prompt for strict decision-making
    prompt = f"""
    You are a very accurate Decision-Making Model, which decides what kind of query is given to you.
    You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation.

    *** Do not answer any query, just classify it. ***

    Rules:
    - Respond with 'general(query) ' if the query can be answered by a conversational AI (e.g., "who was akbar?" → "general who was akbar?").
    - Respond with 'realtime(query)' if the query requires live or up-to-date data (e.g., "what is the weather today?" → "realtime what is the weather today?").
    - Respond with 'automation(query)' if the query is asking to perform an action (e.g., "Open Notepad" → "automation Open Notepad").

    Query: {query}
    Classification:
    """

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=10,
        temperature=0.5  # Keep it deterministic for accuracy
    )
    answer = response.generations[0].text.strip()
    return answer
# print(answer)

    
# elif 'realtime' in answer:
#     ans = realtime.GoogleSearch(answer)
#     mod_ans = realtime.modifyAnswer(ans)
#     print(f"Jarvis: {realtime.getGroqResponse(mod_ans)}")
if __name__ == "__main__":
    while True:
        query = input("User: ")
        if query=='quit':
            break
        answer = classify_query(query)
        # print(classify_query(query))
        if 'general' in answer:
            print(f"Jarvis: {chatbot.get_response(query)}")
        elif 'realtime' in answer:
            print(f"Jarvis: {realtime.main(query)}")
        elif 'automation' in answer:
            print(f"Jarvis: This service will be available soon. :)")