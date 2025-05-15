import openai
from config.credentials import OPENAI_API_KEY 
from openai import OpenAI


# openai.api_key = key


client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are a financial market analyst focused on identifying short-term extremes, rotation flows, and high-probability trade setups from structured indicator data. Your job is to analyze a single timeframe of ETF and index data (e.g., 5M, 1H, 1D) and produce a concise but insightful summary with edge-focused observations.

Use the following format in your response:

1. Money Flow (CMF)
- Top inflows: [ticker (value)], ...
- Top outflows: [ticker (value)], ...
- Highlight significant Z-scores and what they imply.

2. Relative Strength (RSI)
- Overbought (RSI > 65): ...
- Oversold (RSI < 35): ...
- Include RSI Z-scores to highlight extremes and reversion candidates.

3. Volume & OBV
- Tickers with highest relative volume
- OBV Z-score leaders and laggards (e.g., strong accumulation or distribution)

4. Price/Trend Context
- Highlight any meaningful MACD/EMA/RSI or OBV alignment that suggests momentum or weakness.

5. Summary and Trade Setups
- Summarize which sectors or tickers show the clearest strength or weakness.
- Recommend potential setups: momentum, mean reversion, or fade trades.
- Keep it tactical and data-driven, avoid vague language.

Guidelines:
- Do not explain your role or repeat instructions.
- Be concise, confident, and use numeric values when possible.
- Focus on outliers, not averages.
- Lean toward actionability: "X shows strong inflows and breakout potential" or "Y is oversold across CMF and RSI—watch for bounce."
"""



def get_narration(input_text: str, temperature: float = 0.9, model: str = "o4-mini") -> str:
    """
    Sends structured market input to the updated OpenAI analyst and returns a cleaned narration.

    Args:
        input_text (str): Structured user input (e.g. CSV or formatted indicators).
        temperature (float): Creativity setting (not used in current API version).
        model (str): Model to use (default: "o4-mini").

    Returns:
        str: Plain narration text with newlines removed.
    """
    response = client.responses.create(
        model=model,
        input=[{
            "role": "user",
            "content": input_text
        }],
        text={
            "format": {
                "type": "text"
            }
        },
        reasoning={"effort": "medium"},
        tools=[],
        store=True
    )

    try:
        # Access narration content
        narration_text = response.output[1].content[0].text
        cleaned_output = narration_text.replace("\n", " ").strip()
        return cleaned_output
    except (IndexError, AttributeError) as e:
        raise ValueError("Unexpected response format from model.") from e