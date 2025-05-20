import openai
from config.credentials import OPENAI_API_KEY
from openai import OpenAI
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import prompts from separate module
from chatgpt.prompts import ANALYST_PROMPT

# Default configuration
DEFAULT_CONFIG = {
    "model": "o3-mini",
    "temperature": 0.9,
    "store": True
}

# Initialize client once
def get_client():
    """Returns an initialized OpenAI client"""
    return OpenAI(api_key=OPENAI_API_KEY)

client = get_client()

def build_messages(csv_blob: str, system_prompt: str = ANALYST_PROMPT):
    """Build message structure for OpenAI API"""
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

def get_narration(
    csv_blob: str,
    model: str = DEFAULT_CONFIG["model"],
    temperature: float = DEFAULT_CONFIG["temperature"],
    store: bool = DEFAULT_CONFIG["store"],
    timestamp_format: str = '%m/%d/%y - %H:%M'
) -> str:
    """Get narration from OpenAI based on provided CSV data"""
    
    # Generate timestamp if needed for the response
    timestamp = datetime.now().strftime(timestamp_format)
    
    try:
        response = client.responses.create(
            model=model,
            input=build_messages(csv_blob),
            text={"format": {"type": "text"}},
            reasoning={"effort": "medium"},
            tools=[],
            store=store
        )

        # Extract and clean the narration
        narration = response.output[1].content[0].text
        return " ".join(narration.splitlines()).strip()
        
    except Exception as e:
        return f"Error generating narration: {str(e)}"

