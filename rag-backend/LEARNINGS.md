# Portfolio RAG Backend - Post-Mortem & Architecture Learnings

This document logs the critical environment, dependency, and infrastructure gaps encountered during setup to ensure zero friction on future deployments.

---

## 1. The RAG Split: Ingestion vs. Execution
A common trap is assuming that because the backend engine doesn't build the index, it doesn't need the builder's tools. 

* **The Reality:** The data pipeline is split into a **Writer** (`ingest.py`) and a **Reader** (`app/engine.py`). 
* **The Learning:** Even though the Reader *only queries* an existing Qdrant collection, it still must transform the incoming text prompt into a vector using the exact same mathematical model the writer used. 
* **The Fix:** Both environments must explicitly package `llama-index-embeddings-openai` and `llama-index-llms-openai`. If either is missing, LlamaIndex fails implicitly on startup, leading to generic `500 Internal Server Error` responses.

---

## 2. Host Isolation (Bypass the Bleeding Edge)
When developing on host systems with experimental runtimes (e.g., Fedora running pre-release Python 3.14), Python typing and underlying C-extensions (like `pandas` or `pydantic v1` internals) will systematically break.

* **The Learning:** Do not waste hours trying to compile system headers (`Python.h`) or debug upstream framework code on an unsupported host runtime.
* **The Fix:** Immediately isolate local scripts (like ingestion) using a production-stable container runtime mapped to your working directory:
  ```bash
  docker run -it --rm \
    -v "$(pwd)":/app -w /app \
    -e QDRANT_URL="..." -e QDRANT_API_KEY="..." -e OPENAI_API_KEY="..." \
    python:3.11-slim \
    sh -c "pip install -r requirements.txt llama-index-readers-file llama-index-embeddings-openai && python ingest.py"


3. Google Cloud Platform (GCP) Secure-by-Default Traps
On any newly provisioned GCP Project (like axiomatic-spark-505611-t0), Google's updated security postures intentionally cripple the default Service Accounts to prevent supply-chain vulnerabilities.

The Learning: Direct source deployments (gcloud run deploy --source .) will consistently fail at the "Building Container" phase on fresh projects until the infrastructure service account is explicitly unshackled.

The Fix: Before building, ensure the project's default compute service account ({PROJECT_NUMBER}-compute@developer.gserviceaccount.com) is manually bound to these strict IAM roles:

Bash
# Grant Cloud Build orchestration management
gcloud projects add-iam-policy-binding [PROJECT_ID] \
    --member="serviceAccount:[PROJECT_NUMBER]-compute@developer.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

# Grant access to pull the uploaded source zip from Cloud Storage
gcloud projects add-iam-policy-binding [PROJECT_ID] \
    --member="serviceAccount:[PROJECT_NUMBER]-compute@developer.gserviceaccount.com" \
    --role="roles/storage.objectViewer"
4. Source Directory Structure Constraints
When configuring directory readers for unstructured text ingestion:

SimpleDirectoryReader("data", recursive=True) effortlessly handles complex folder mapping (data/experience/, data/projects/).

The Catch: This recursion must happen during the Ingestion phase (ingest.py). The production API context should remain entirely decoupled from the raw data/ folder, relying solely on the remote vector database connection strings.
