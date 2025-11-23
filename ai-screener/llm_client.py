import os
import json
from dotenv import load_dotenv

load_dotenv()  # loads OPENAI_API_KEY from .env if present

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# If user has OpenAI key, import openai
if OPENAI_KEY:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)


async def call_openai(question: str, answer: str):
    """
    Calls OpenAI model to get score, summary, improvement.
    If API key missing → this function won't be used.
    """
    prompt = f"""
You are an expert interviewer.

Evaluate the candidate's answer and return STRICT JSON:
{{
  "score": 1-5,
  "summary": "one line summary",
  "improvement": "one suggestion"
}}

Question: {question}
Answer: {answer}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return only pure JSON."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0,
    )

    text = response.choices[0].message.content.strip()

    # Extract JSON from response
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        return json.loads(json_text)
    except Exception:
        raise ValueError(f"Model did not return pure JSON: {text}")


def fallback_evaluator(question: str, answer: str):
    """
    Simple rule-based scoring — used if OpenAI_KEY is missing.
    """
    ans = answer.lower()

    if len(ans) < 10:
        score = 1
    elif len(ans) < 25:
        score = 2
    elif len(ans) < 50:
        score = 3
    elif len(ans) < 100:
        score = 4
    else:
        score = 5

    return {
        "score": score,
        "summary": answer[:60] + "...",
        "improvement": "Add more clarity and structure in your answer."
    }


async def evaluate_llm(question: str, answer: str):
    """
    Tries OpenAI → fallback if no API key.
    """
    if OPENAI_KEY:
        try:
            return await call_openai(question, answer)
        except Exception as e:
            print("OpenAI failed. Using fallback.", e)

    return fallback_evaluator(question, answer)
