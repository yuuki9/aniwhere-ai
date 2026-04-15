from __future__ import annotations

import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

from app.config import get_settings


def _collection():
    settings = get_settings()
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=settings.openai_api_key,
        model_name=settings.openai_embedding_model,
    )
    client = chromadb.PersistentClient(path=settings.chroma_path)
    return client.get_collection(
        name=settings.collection_name,
        embedding_function=ef,
    )


def retrieve_context(query: str, top_k: int | None = None) -> str:
    settings = get_settings()
    k = top_k if top_k is not None else settings.rag_top_k
    col = _collection()
    result = col.query(query_texts=[query], n_results=k)
    docs = (result.get("documents") or [[]])[0]
    metas = (result.get("metadatas") or [[]])[0]
    ids = (result.get("ids") or [[]])[0]
    if not docs:
        return ""

    blocks: list[str] = []
    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        sid = ids[i] if i < len(ids) else str(i)
        meta_s = ", ".join(f"{k}={v}" for k, v in (meta or {}).items())
        blocks.append(f"[{sid}] ({meta_s})\n{doc}")
    return "\n\n---\n\n".join(blocks)


def rag_answer(user_query: str) -> tuple[str, str]:
    settings = get_settings()
    context = retrieve_context(user_query)
    client = OpenAI(api_key=settings.openai_api_key)

    if not context.strip():
        system = (
            "너는 가챠샵·애니 굿즈 안내 도우미다. "
            "벡터 DB에서 가져온 근거 문서가 없다면, 추측하지 말고 "
            "데이터에 해당 정보가 없다고 짧게 말해라."
        )
        user_content = f"사용자 질문:\n{user_query}"
    else:
        system = (
            "너는 가챠샵·애니 굿즈 안내 도우미다. "
            "반드시 아래 [근거 문서] 안의 내용만 사용해 답해라. "
            "근거에 없는 사실은 지어내지 말고, 부족하면 '문서에 명시되지 않음'이라고 해라. "
            "답변은 한국어로, 매장 이름·지역·캐릭터/상품 여부를 구분해 알기 쉽게 정리해라."
        )
        user_content = f"[근거 문서]\n{context}\n\n[질문]\n{user_query}"

    completion = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
    )
    answer = (completion.choices[0].message.content or "").strip()
    return answer, context
