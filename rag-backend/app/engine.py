import os
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai import OpenAI

class RAGEngine:
    def __init__(self):
        self._query_engine = None

    def _get_engine(self):
        if self._query_engine is None:
            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")
            openai_api_key = os.getenv("OPENAI_API_KEY")

            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            vector_store = QdrantVectorStore(client=client, collection_name="portfolio-corpus")
            llm = OpenAI(model="gpt-4o-mini", temperature=0.1, api_key=openai_api_key)

            index = VectorStoreIndex.from_vector_store(vector_store=vector_store, llm=llm)
            self._query_engine = index.as_query_engine(similarity_top_k=3)
        return self._query_engine

    def query(self, prompt: str) -> str:
        engine = self._get_engine()
        response = engine.query(prompt)
        return str(response)

rag_engine = RAGEngine()