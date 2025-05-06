# Jarvis

## Description

Jarvis is a personal assistant project inspired by the fictional AI from Iron Man. It integrates real-time query handling using the Groq API, casual conversations via the Cohere API, and intent classification to route queries appropriately, with web search capabilities via Yep.com. A frontend interface is planned for future development.

## Installation

```bash
# Clone the repository
git clone https://github.com/gourabanandad/Jarvis.git
cd Jarvis

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your GroqAPI, CohereAPI, User, and Assistantname
```

## Usage

```bash
# Run the main script
python main.py

# Example queries
# General: "Who was Akbar?"
# Real-time: "What's the weather today?"
# Automation: "Open Notepad" (coming soon)
# Type 'quit' to exit
```

## Features

* **Intent Classification**: Uses Cohere API to classify queries as general, real-time, or automation.
* **Real-Time Queries**: Uses Groq API with Yep.com search for accurate, professional responses.
* **Casual Conversations**: Leverages Cohere API for human-like, concise chats.
* **Web Search Integration**: Fetches real-time data using Yep.com for up-to-date information.
* **Customizable Assistant**: Configurable username and assistant name via environment variables.
* **Indian Context**: Tailored for Indian users with date awareness.
* **Future Frontend**: A user interface is planned for future integration.

## Code Overview

### Intent Classification

* Uses `cohere` library to classify queries into general, realtime, or automation.
* Example: `classify_query("What's the weather today?")` returns `realtime(What's the weather today?)`.
* Routes queries to appropriate handlers based on classification.
* **Cohere API Docs**: [https://docs.cohere.com](https://docs.cohere.com)

### Real-Time Queries

* Uses `groq` library to interact with Groq API for professional responses.
* Web scraping with `requests` and `BeautifulSoup` to fetch search results from Yep.com.
* Example: `main("Tell me some special things about today?")`.
* **Groq API Docs**: [https://groq.com/docs](https://groq.com/docs)

### Casual Chat

* Uses `cohere` library for human-like responses.
* Configurable prompt for concise, English-only responses.
* Example: `get_response("What is your name?")`.

### Main Loop

* Continuously accepts user input via command line and classifies queries.
* Routes to `get_response` for general queries, `main` for real-time queries, or displays a placeholder for automation.
* Exits on `quit` command.

## Requirements

* Python 3.8+
* Libraries: `groq`, `cohere`, `requests`, `beautifulsoup4`, `python-dotenv`, `duckduckgo_search`
* API Keys: Groq API, Cohere API

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

GitHub: [gourabanandad](https://github.com/gourabanandad)
