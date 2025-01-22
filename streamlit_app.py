"""
NeuroChatAI - A Streamlit-based interface for local LLM interaction
Version: 1.0.0
Created: 2025-01-22 
Author: Cs944612
Repository: https://github.com/Cs944612/NeuroChatAI
"""

import streamlit as st
import requests
from typing import Dict, List, Optional
import time
from datetime import datetime
import logging
import json
from dotenv import load_dotenv    
import os

# Load environment variables
load_dotenv()

# Application Constants
APP_VERSION = "1.0.0"
APP_NAME = "NeuroChatAI"
GITHUB_REPO = "https://github.com/Cs944612/NeuroChatAI"
CREATED_DATE = "2025-01-22 16:10:37 UTC"
AUTHOR = "Cs944612"

# Enhanced Constants
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:1234/v1/completions")
DEFAULT_MODEL_NAME = os.getenv("MODEL_NAME", "your-model-name")
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "5"))
RATE_LIMIT_SECONDS = float(os.getenv("RATE_LIMIT_SECONDS", "1.0"))

# Predefined Prompts
PREDEFINED_PROMPTS = [
    "Tell me a joke about programming.",
    "Explain how APIs work in simple terms.",
    "Write a short Python function to calculate fibonacci numbers.",
    "What are the best practices for code documentation?",
    "Generate a creative story about AI and humans working together.",
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

def get_app_info() -> Dict[str, str]:
    """Return application information"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "created": CREATED_DATE,
        "author": AUTHOR,
        "repository": GITHUB_REPO
    }

def initialize_session_state() -> None:
    """Initialize the session state variables"""
    default_states = {
        "messages": [],
        "api_health": True,
        "last_api_check": None,
        "system_prompt": """You are a helpful AI assistant. 
        You provide clear, accurate, and concise responses while being friendly and professional.""",
        "chat_style": "modern",
        "last_request_time": 0
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def check_api_health(api_url: str) -> bool:
    """
    Check if the API endpoint is accessible
    
    Args:
        api_url (str): The API endpoint URL
    
    Returns:
        bool: True if API is healthy, False otherwise
    """
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validate_api_url(api_url: str) -> bool:
    """
    Validate the format of the API URL
    
    Args:
        api_url (str): The API URL to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        result = requests.utils.urlparse(api_url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def display_chat_history() -> None:
    """Display the chat history with improved formatting"""
    st.write("### 💬 Chat")
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def rate_limit_check() -> bool:
    """
    Implement basic rate limiting
    
    Returns:
        bool: True if within rate limit, False otherwise
    """
    current_time = time.time()
    if current_time - st.session_state["last_request_time"] < RATE_LIMIT_SECONDS:
        st.warning(f"Please wait {RATE_LIMIT_SECONDS} seconds between messages.")
        return False
    
    st.session_state["last_request_time"] = current_time
    return True

def send_request_to_model(api_url: str, payload: Dict) -> Optional[Dict]:
    """
    Send a request to the local model API with improved error handling
    
    Args:
        api_url (str): The API endpoint URL
        payload (Dict): The request payload
    
    Returns:
        Optional[Dict]: The API response or None if request fails
    """
    try:
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        logger.error("API request timed out")
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        logger.error(f"API request failed: {str(e)}")
    except json.JSONDecodeError:
        st.error("Invalid response from API")
        logger.error("Failed to decode API response")
    return None

def build_prompt_with_history(user_input: str) -> str:
    """
    Build a prompt including chat history with improved formatting
    
    Args:
        user_input (str): The user's input message
    
    Returns:
        str: The formatted prompt with history
    """
    history = []
    
    # Add system prompt if exists
    if st.session_state.get("system_prompt"):
        history.append(f"System: {st.session_state['system_prompt']}\n")
    
    # Add recent message history
    for msg in st.session_state["messages"][-MAX_HISTORY_MESSAGES:]:
        role = "Human:" if msg["role"] == "user" else "Assistant:"
        history.append(f"{role} {msg['content']}")
    
    history.append(f"Human: {user_input}")
    return "\n".join(history) + "\nAssistant:"

def handle_user_input(
    user_input: str,
    api_url: str,
    model_name: str,
    temperature: float,
    max_tokens: int
) -> None:
    """
    Process user input and get model response with improved error handling
    
    Args:
        user_input (str): The user's input message
        api_url (str): The API endpoint URL
        model_name (str): The name of the model
        temperature (float): The temperature parameter for generation
        max_tokens (int): Maximum number of tokens to generate
    """
    if not rate_limit_check():
        return

    if not user_input.strip():
        st.warning("Please enter a non-empty message.")
        return

    # Add user input to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        prompt = build_prompt_with_history(user_input)
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model": model_name,
            "stop": ["\nHuman:", "\n\nHuman:", "\nSystem:"]
        }

        response = send_request_to_model(api_url, payload)
        
        if response and "choices" in response and response["choices"]:
            ai_message = response["choices"][0]["text"].strip()
            st.session_state["messages"].append({"role": "assistant", "content": ai_message})
            
            with st.chat_message("assistant"):
                st.write(ai_message)
        else:
            st.error("Failed to get a valid response from the model.")

def export_chat_history() -> None:
    """Export chat history to a JSON file"""
    if st.session_state["messages"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        chat_data = {
            "app_info": get_app_info(),
            "timestamp": timestamp,
            "messages": st.session_state["messages"],
            "system_prompt": st.session_state.get("system_prompt", "")
        }
        st.download_button(
            label="📤 Export Chat",
            data=json.dumps(chat_data, indent=2),
            file_name=filename,
            mime="application/json"
        )

def sidebar_settings() -> tuple:
    """
    Display and handle sidebar settings with validation
    
    Returns:
        tuple: (api_url, model_name, temperature, max_tokens)
    """
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Add tabs for different settings categories
        tab1, tab2, tab3 = st.tabs(["Model", "Chat", "System"])
        
        with tab1:
            api_url = st.text_input(
                "API Endpoint",
                DEFAULT_API_URL,
                help="The API endpoint for your local model."
            )
            
            if not validate_api_url(api_url):
                st.warning("Please enter a valid API URL")
            
            model_name = st.text_input(
                "Model Name",
                DEFAULT_MODEL_NAME,
                help="The name of the model you're using."
            )
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Controls the randomness of the model's responses."
            )
            
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=10,
                max_value=4096,
                value=512,
                help="The maximum number of tokens to generate."
            )
        
        with tab2:
            st.number_input(
                "Max History Messages",
                min_value=1,
                max_value=20,
                value=MAX_HISTORY_MESSAGES,
                help="Number of previous messages to include for context"
            )
            
            st.number_input(
                "Rate Limit (seconds)",
                min_value=0.1,
                max_value=5.0,
                value=RATE_LIMIT_SECONDS,
                step=0.1,
                help="Minimum time between messages"
            )
        
        with tab3:
            system_prompt = st.text_area(
                "System Prompt",
                st.session_state.get("system_prompt", ""),
                help="Define the AI assistant's behavior"
            )
            if st.button("Update System Prompt"):
                st.session_state["system_prompt"] = system_prompt
                st.success("System prompt updated!")

        # Predefined prompts section
        st.markdown("---")
        st.header("💡 Quick Prompts")
        for prompt in PREDEFINED_PROMPTS:
            if st.button(prompt):
                handle_user_input(prompt, api_url, model_name, temperature, max_tokens)

        # App info and controls
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Reset Chat"):
                st.session_state["messages"] = []
                st.success("Chat history has been reset.")
        with col2:
            export_chat_history()
        
        # App information
        st.markdown("---")
        app_info = get_app_info()
        st.markdown(f"**{app_info['name']}** v{app_info['version']}")
        st.markdown(f"[GitHub Repository]({app_info['repository']})")

        return api_url, model_name, temperature, max_tokens

def main():
    """Main application function with error handling and session management"""
    try:
        # Set up the Streamlit app
        st.set_page_config(
            page_title=APP_NAME,
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title(f"🧠 {APP_NAME}")
        st.markdown("""
        Welcome to NeuroChatAI! This interface allows you to interact with your local language model.
        Configure your settings in the sidebar and start chatting below.
        """)

        # Initialize session state
        initialize_session_state()

        # Display settings in the sidebar
        api_url, model_name, temperature, max_tokens = sidebar_settings()

        # Create chat container
        chat_container = st.container()
        with chat_container:
            display_chat_history()

        # Get and handle user input
        user_input = st.chat_input("Your message")
        if user_input:
            handle_user_input(user_input, api_url, model_name, temperature, max_tokens)

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()