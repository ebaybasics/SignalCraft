import logging
from config.credentials import OPENAI_API_KEY
from openai import OpenAI
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# Import all available prompts from prompts module
from chatgpt.prompts import ANALYST_PROMPT, TICKER_ANALYST_PROMPT, BEST_SECTOR_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Available prompts dictionary for easy lookup
AVAILABLE_PROMPTS = {
    "market": ANALYST_PROMPT,
    "ticker": TICKER_ANALYST_PROMPT,
    "sector": BEST_SECTOR_PROMPT
}

# Default configuration
DEFAULT_CONFIG = {
    "model": "o3-mini",
    "temperature": 0.9,
    "store": True,
    "prompt_type": "market"  # Default to market analysis prompt
}

# Model-specific configurations
MODEL_CONFIGS = {
    "o3-mini": {
        "api_type": "responses",
        "supports_reasoning": True
    },
    "o4-mini": {
        "api_type": "responses", 
        "supports_reasoning": True
    },
    "gpt-4o": {
        "api_type": "chat_completions",
        "supports_reasoning": False
    },
    "gpt-4": {
        "api_type": "chat_completions",
        "supports_reasoning": False
    },
    "gpt-3.5-turbo": {
        "api_type": "chat_completions",
        "supports_reasoning": False
    }
}

# Initialize client once
def get_client():
    """Returns an initialized OpenAI client"""
    return OpenAI(api_key=OPENAI_API_KEY)

# Create a singleton client instance
client = get_client()

def get_prompt(prompt_type: str = DEFAULT_CONFIG["prompt_type"]) -> str:
    """Get the prompt template by type
    
    Args:
        prompt_type: Type of prompt to use (market, ticker)
        
    Returns:
        The prompt template string
    """
    return AVAILABLE_PROMPTS.get(prompt_type, ANALYST_PROMPT)

def build_messages_responses(csv_blob: str, prompt_type: str = DEFAULT_CONFIG["prompt_type"]):
    """Build message structure for OpenAI Responses API
    
    Args:
        csv_blob: CSV data to analyze
        prompt_type: Type of prompt to use
        
    Returns:
        List of message objects formatted for Responses API
    """
    system_prompt = get_prompt(prompt_type)
    return [
        {
            "role": "system",
            "content": [
                {"type": "input_text", "text": system_prompt.strip()}
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": csv_blob.strip()}
            ],
        },
    ]

def build_messages_chat(csv_blob: str, prompt_type: str = DEFAULT_CONFIG["prompt_type"]):
    """Build message structure for OpenAI Chat Completions API
    
    Args:
        csv_blob: CSV data to analyze
        prompt_type: Type of prompt to use
        
    Returns:
        List of message objects formatted for Chat Completions API
    """
    system_prompt = get_prompt(prompt_type)
    return [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": csv_blob.strip()}
    ]

def get_narration(
    csv_blob: str,
    model: str = DEFAULT_CONFIG["model"],
    temperature: float = DEFAULT_CONFIG["temperature"],
    store: bool = DEFAULT_CONFIG["store"],
    prompt_type: str = DEFAULT_CONFIG["prompt_type"],
    timestamp_format: str = '%m/%d/%y - %H:%M'
) -> Union[str, Dict[str, Any]]:
    """Get narration from OpenAI based on provided CSV data
    
    Args:
        csv_blob: CSV data to analyze
        model: OpenAI model to use
        temperature: Temperature parameter for generation
        store: Whether to store the response
        prompt_type: Type of prompt to use (market, ticker)
        timestamp_format: Format for timestamp in response
        
    Returns:
        Narration string or error dictionary
    """
    
    # Generate timestamp for the response
    timestamp = datetime.now().strftime(timestamp_format)
    
    try:
        logger.info(f"Requesting narration using model {model} with {prompt_type} prompt")
        
        # Get model configuration or use default for chat completions
        model_config = MODEL_CONFIGS.get(model, {"api_type": "chat_completions", "supports_reasoning": False})
        api_type = model_config["api_type"]
        
        if api_type == "responses":
            # Handle Responses API for reasoning models
            params = {
                "model": model,
                "input": build_messages_responses(csv_blob, prompt_type),
                "text": {"format": {"type": "text"}},
                "tools": [],
                "store": store
            }
            
            # Add reasoning parameter only if supported
            if model_config["supports_reasoning"]:
                params["reasoning"] = {"effort": "medium"}
            
            response = client.responses.create(**params)
            narration = response.output[1].content[0].text
            
        else:
            # Handle Chat Completions API for chat models
            response = client.chat.completions.create(
                model=model,
                messages=build_messages_chat(csv_blob, prompt_type),
                temperature=temperature
            )
            narration = response.choices[0].message.content
        
        # Clean and format the narration
        formatted_narration = " ".join(narration.splitlines()).strip()
        return formatted_narration
        
    except Exception as e:
        logger.error(f"Error generating narration: {str(e)}")
        # Return structured error for better handling in run_narration_test.py
        return {
            "error": str(e),
            "timestamp": timestamp,
            "success": False
        }

