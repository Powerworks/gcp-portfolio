import os
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore

def run_ingestion():
    print("Reading documents from data/ directory (including subfolders)...")
    # This automatically searches recursively down through folders!
    documents = SimpleDirectoryReader("data", recursive=True).load_data()
    print(f"Loaded {len(documents)} document sections.")

    # Grab your environment variables
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("Error: Please export QDRANT_URL and QDRANT_API_KEY to your terminal first.")
        return

    print("Connecting to Qdrant Cloud...")
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    print("Setting up Vector Store for 'portfolio-corpus'...")
    vector_store = QdrantVectorStore(client=client, collection_name="portfolio-corpus")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("Generating embeddings via OpenAI and uploading to cloud...")
    # This builds the collection and uploads it using your local environment variables
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context
    )
    print("Success! Your Qdrant Cloud cluster has been fully populated.")

if __name__ == "__main__":
    run_ingestion()
