# 🤖 Jarvis - Your Personal AI Assistant

![Jarvis Banner](https://github.com/gourabanandad/Jarvis/blob/571af57414182e05e160b1cf49d7ddb38061ffcb/banner.png)


A sophisticated personal assistant inspired by the iconic AI from Iron Man, combining cutting-edge APIs with intelligent query routing.

## ✨ Features

| Feature                       | Description                                          | Status        |
| ----------------------------- | ---------------------------------------------------- | ------------- |
| **🧠 Intent Classification**  | Smart query routing using Cohere API                 | ✅ Implemented |
| **⚡ Real-Time Queries**       | Professional responses via Groq API + Yep.com search | ✅ Implemented |
| **🗬️ Casual Conversations**  | Human-like chats using Cohere API                    | ✅ Implemented |
| **🌐 Web Search Integration** | Real-time data from Yep.com                          | ✅ Implemented |
| **🇮🇳 Indian Context**       | Tailored for Indian users with date awareness        | ✅ Implemented |
| **🎨 Future Frontend**        | Planned GUI interface                                | ⌛ Coming Soon |

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* API keys for [Groq](https://groq.com/) and [Cohere](https://cohere.com/)

### Installation

```bash
# Clone and setup
git clone https://github.com/gourabanandad/Jarvis.git
cd Jarvis

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and preferences
```

### Usage

```bash
python main.py

Try these example queries:
• "Who was Akbar?"
• "What's the weather today?"
• "Tell me about quantum computing"
• Type 'quit' to exit
```

## 🧹 Core Components

### 1. Intent Classification

```python
# Example classification
query = "What's the weather today?"
intent = classify_query(query)  # Returns 'realtime'
```

### 2. Real-Time Query Processing

```python
# Professional response generation
response = groq_client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[{"role": "user", "content": query}]
)
```

### 3. Casual Conversation

```python
# Human-like chat response
response = cohere_client.generate(
    model="command",
    prompt=f"User: {query}\nAssistant:",
    max_tokens=300
)
```

## 📂 Project Structure

```
Jarvis/
├── .env                  # Environment variables
├── .gitignore            # Git ignored files
├── README.md             # Project documentation
├── main.py               # Entry point for the assistant
├── requirements.txt      # Python dependencies
├── structure.txt         # Project file structure (this file!)
├── desktop.ini           # Windows desktop config file

├── Backend/
│   ├── automation.py             # Background automation logic
│   ├── chatbot.py                # Chatbot controller logic
│   ├── ImageGeneration.py       # AI image generation logic
│   ├── intent_classifier.py     # Intent classification logic (Cohere/BERT)
│   ├── model.py                 # LLM interaction setup
│   ├── realtime.py              # Real-time search with Groq + Yep
│   ├── SpeechToText.py          # Voice input handling
│   ├── TextToSpeech.py          # Converts output to speech
│   ├── tempCodeRunnerFile.py    # Temporary file (can be deleted)
│
│   ├── bert_intent_classifier/  # BERT model files
│   │   ├── config.json
│   │   ├── model.safetensors
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   └── vocab.txt
│
│   └── __pycache__/             # Compiled bytecode (auto-generated)

├── Frontend/
│   └── ImageGeneration.data     # Data placeholder (GUI planned)
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

**Gourab Anand**

* GitHub: [@gourabanandad](https://github.com/gourabanandad)
* LinkedIn: [@yourhandle](https://www.linkedin.com/in/gourabananda-datta-a3521a285?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) 
* Email: [gourabanandad@gmail.com](mailto:gourabanandad@gmail.com) 

---

<div align="center">
Made with ❤️ and Python
</div>
