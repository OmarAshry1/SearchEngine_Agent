import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool  
from ddgs import DDGS 
import arxiv  
import os
from dotenv import load_dotenv

load_dotenv()


def duckduckgo_search(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=1))
        return results[0] if results else "No results found."


def arxiv_search(query: str) -> str:
    client = arxiv.Client()
    results = list(client.results(arxiv.Search(query=query, max_results=1)))
    return results[0].summary if results else "No results found."


tools = [
    Tool(
        name="DuckDuckGo_Search",
        func=duckduckgo_search,
        description="Useful for general web searches about current events, products, or recent information. Use this as your primary search tool."
    ),
    Tool(
        name="Arxiv_Search",
        func=arxiv_search,
        description="Specifically for searching academic and scientific papers. Only use this for academic or research-related queries."
    ),
    Tool(
        name="Wikipedia",
        func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1)),
        description="Use this for getting detailed background information about well-established topics, concepts, or historical information."
    )
]


st.title("🔎 LangChain - Chat with Search")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if api_key:
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="Llama3-8b-8192",
            streaming=True,
            temperature=0.3  # Add lower temperature for more focused responses
        )
        agent = initialize_agent(
            tools, 
            llm, 
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            max_iterations=2,  # Limit the number of tool uses
            early_stopping_method="generate"  # Stop if the agent is looping
        )
        
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = agent.run({"input": prompt}, callbacks=[st_cb]) 
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
    else:
        st.warning("Please enter a Groq API key.")