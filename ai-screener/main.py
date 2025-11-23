from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import asyncio
from scorer import evaluate_answer_payload

app = FastAPI(
    title="Mini AI Screener",
    description="A lightweight backend to evaluate and rank candidate answers using LLM or fallback scoring.",
    version="1.0.0"
)

# -----------------------------
# REQUEST MODELS WITH EXAMPLES
# -----------------------------

class EvalRequest(BaseModel):
    answer: str = Field(
        ...,
        title="Candidate Answer",
        description="Full answer from the candidate. Prefer format: 'Candidate says: <text>'.",
        example="Candidate says: I would design the API using REST principles, proper HTTP methods, and a PostgreSQL database."
    )

    question: str = Field(
        "General interview question",
        title="Question",
        description="The question being asked to the candidate (optional).",
        example="How would you design a CRUD API?"
    )


class Candidate(BaseModel):
    id: str = Field(
        ...,
        title="Candidate ID",
        example="candidate_101",
        description="Unique identifier for the candidate."
    )

    answer: str = Field(
        ...,
        title="Candidate Answer",
        example="Candidate says: REST APIs use HTTP methods such as GET, POST, PUT, DELETE.",
        description="Candidate’s answer to evaluate."
    )

    question: str = Field(
        "General interview question",
        example="Explain REST APIs.",
        description="The question asked to the candidate (optional)."
    )


# -----------------------------
# ENDPOINTS
# -----------------------------

@app.post(
    "/evaluate-answer",
    summary="Evaluate a single candidate answer",
    description="Returns a score (1–5), a one-line summary, and an improvement suggestion."
)
async def evaluate_answer(req: EvalRequest):
    result = await evaluate_answer_payload(req.dict())
    return result


@app.post(
    "/rank-candidates",
    summary="Evaluate and rank multiple candidates",
    description="Evaluates each candidate answer and returns them sorted by highest score."
)
async def rank_candidates(candidates: List[Candidate]):
    tasks = [evaluate_answer_payload(c.dict()) for c in candidates]
    results = await asyncio.gather(*tasks)

    ranked = [
        {
            "id": candidates[i].id,
            "score": results[i]["score"],
            "summary": results[i]["summary"],
            "improvement": results[i]["improvement"]
        }
        for i in range(len(candidates))
    ]

    ranked.sort(key=lambda x: -x["score"])
    return ranked


@app.get(
    "/health",
    summary="Health check",
    description="Returns status OK if the server is running"
)
def health():
    return {"status": "ok"}
