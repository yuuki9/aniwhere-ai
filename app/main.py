from __future__ import annotations

from contextlib import asynccontextmanager

from chromadb.errors import NotFoundError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.rag import rag_answer


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="예: 홍대에 고죠사토루가 있는 가챠샵을 알려줘")


class AskResponse(BaseModel):
    answer: str
    context_used: str = Field(
        ...,
        description="LLM에 전달된 근거 문자열(디버그·감사용). 운영에서는 숨길 수 있음.",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Aniwhere RAG API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/ask", response_model=AskResponse)
def ask(body: AskRequest):
    q = body.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="query is empty")
    try:
        answer, context = rag_answer(q)
    except NotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail="벡터 DB 컬렉션이 없습니다. 먼저 `python -m app.ingest` 로 데이터를 넣으세요.",
        ) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"upstream error: {e!s}") from e
    return AskResponse(answer=answer, context_used=context)
