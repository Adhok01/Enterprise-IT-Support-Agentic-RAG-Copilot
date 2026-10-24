from app.services.ingestion import load_file, chunk_documents
from app.rag.vectorstore import add_documents

from pathlib import Path


doc = load_file(Path("data/company_it_handbook.md"))
chunks = chunk_documents(doc)
 
add_documents(chunks)
