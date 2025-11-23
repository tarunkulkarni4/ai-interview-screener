from llm_client import evaluate_llm

async def evaluate_answer_payload(payload):
    """
    Expected payload:
    { "answer": "Candidate says: <text>", "question": "optional" }
    """
    raw = payload.get("answer", "")
    question = payload.get("question", "General interview question")

    # Remove prefix "Candidate says:"
    if raw.lower().startswith("candidate says:"):
        raw = raw.split(":", 1)[1].strip()

    result = await evaluate_llm(question, raw)

    return {
        "score": int(result["score"]),
        "summary": result["summary"],
        "improvement": result["improvement"]
    }
