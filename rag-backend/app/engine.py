import os
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai import OpenAI

class RAGEngine:
    def __init__(self):
        # 1. Resolve secrets natively from the Cloud Run environment
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # 2. Initialize a zero-overhead native Qdrant Client
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )
        
        # 3. Bind to your high-fidelity portfolio documentation collection
        self.vector_store = QdrantVectorStore(
            client=self.client, 
            collection_name="portfolio-corpus"
        )
        
        # 4. Set up storage context and enforce strict compute budget caps
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.llm = OpenAI(model="gpt-4o-mini", temperature=0.1) # Low cost, high semantic accuracy

    def query(self, prompt: str) -> str:
        # Reconstruct index dynamically from vector space with no heavy on-disk footprint
        index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            llm=self.llm
        )
        query_engine = index.as_query_engine(similarity_top_k=3)
        response = query_engine.query(prompt)
        return str(response)

# Instantiate engine as a reusable application-level singleton
rag_engine = RAGEngine()