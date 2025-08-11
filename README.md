# LangChain Search Engine

A powerful multi-source search engine built with LangChain that combines DuckDuckGo, Arxiv, and Wikipedia searches using an AI agent.

## 🌟 Features

- **Multiple Search Sources**:
  - DuckDuckGo for general web searches
  - Arxiv for academic papers
  - Wikipedia for comprehensive background information

- **AI-Powered**: Uses Groq's LLM to intelligently process and combine search results
- **Interactive UI**: Built with Streamlit for a seamless user experience
- **Streaming Responses**: Real-time response streaming as the agent works

## 🚀 Installation

```sh
# Clone the repository
git clone <repository-url>
cd SearchEngine

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Configuration

1. Get a Groq API key from [Groq's platform](https://www.groq.com)
2. Add your API key in the Streamlit sidebar when running the application

## 📦 Dependencies

```text
streamlit
langchain
langchain-groq
wikipedia
python-dotenv
duckduckgo-search
arxiv
```

## 🏃‍♂️ Usage

```sh
streamlit run app.py
```

The app will start on `http://localhost:8501`

## 🔍 How It Works

1. Enter your query in the chat interface
2. The AI agent analyzes your question
3. Selects the most appropriate search source(s)
4. Returns a comprehensive answer combining the search results

## 🛠️ Technical Details

- Uses LangChain's Agent framework for tool selection
- Implements Zero-Shot-React-Description agent type
- Includes early stopping and iteration limits for efficient searches
- Streaming support for real-time response generation

