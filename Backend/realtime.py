from groq import Groq
import os
import time
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import datetime as dt
load_dotenv()

Username = os.getenv('User')
Assistantname = os.getenv('Assistantname')
client = Groq(api_key=os.getenv('GroqAPI'))
day = dt.datetime.now().day
month = dt.datetime.now().strftime("%B")
year = dt.datetime.now().year
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Today's date is {day} {month} of {year}.***
*** Always remember I am an Indian.***
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***
*** Please read the whole thing and always give to the point answer. ***"""

# def GoogleSearch(query):
#     # with DDGS() as ddgs:
#     #     results = list(ddgs.text(query, max_results=5))
#     # answer = f"The search result for '{query}' are: \n[start]\n"
#     # for i in results:
#     #     answer+=f"Title: {i['title']}\nSnippet: {i['body']}\nURL: {i['href']}\n\n"
#     # answer+="[end]"
#     # return answer
#     headers = {"User-Agent": "Mozilla/5.0"}
#     url = f"https://www.google.com/search?q={query}"
#     res = requests.get(url, headers=headers)
#     soup = BeautifulSoup(res.text, "html.parser")
    
#     answer = f"The search result for '{query}' are: \n[start]\n"
#     for g in soup.select(".tF2Cxc"):  # CSS selector may change!
#         title = g.select_one("h3").text
#         snippet = g.select_one(".IsZvec").text
#         link = g.a["href"]
#         answer += f"Title: {title}\nSnippet: {snippet}\nURL: {link}\n\n"
#     answer += "[end]"
#     return answer


    
def YepSearch(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.yep.com/search?q={query}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    answer = f"Results for '{query}':\n[start]\n"
    for result in soup.select(".result"):  # Check actual CSS selectors
        title = result.select_one("h3").text
        snippet = result.select_one(".snippet").text
        link = result.a["href"]
        answer += f"Title: {title}\nSnippet: {snippet}\nURL: {link}\n\n"
    answer += "[end]"
    return answer


def modifyAnswer(answer):
    lines = answer.split('\n')
    non_empty_line = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_line)
    return modified_answer

def getGroqResponse(user_query, raw_search_results):
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": System},
            {"role": "user", "content": f"Query: {user_query}\n\n{raw_search_results}"}
        ]
    )
    return chat_completion.choices[0].message.content
    

def main(query):
    ans = YepSearch(query)
    m_ans = modifyAnswer(ans)
    return getGroqResponse(query, m_ans)
# query = "Tell me some special things about today?"
# ans = YepSearch(query)
# print(ans)
# m_ans = modifyAnswer(ans)
# print(m_ans)
# print(getGroqResponse(query, m_ans))
