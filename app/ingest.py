"""Chroma 컬렉션에 샘플 문서를 넣는 스크립트. 실행: python -m app.ingest"""

from __future__ import annotations

import chromadb
from chromadb.utils import embedding_functions

from app.config import get_settings
from app.seed_data import DOCUMENTS


def main() -> None:
    settings = get_settings()
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=settings.openai_api_key,
        model_name=settings.openai_embedding_model,
    )
    client = chromadb.PersistentClient(path=settings.chroma_path)
    col = client.get_or_create_collection(
        name=settings.collection_name,
        embedding_function=ef,
    )

    ids = [d["id"] for d in DOCUMENTS]
    texts = [d["text"] for d in DOCUMENTS]
    metadatas = [d.get("metadata") or {} for d in DOCUMENTS]

    col.upsert(ids=ids, documents=texts, metadatas=metadatas)
    print(f"Upserted {len(ids)} documents into '{settings.collection_name}' at {settings.chroma_path}")


if __name__ == "__main__":
    main()
