from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from typing import List, Dict

class VectorStore:
    def __init__(self):
        # Ensure the API key is passed correctly
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing.")
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
    
    def add_texts(self, contents: List[Dict[str, str]]) -> None:
        texts = [f"File: {c['path']}\n\n{c['content']}" for c in contents]
        self.db.add_texts(
            texts,
            metadatas=[{"source": c["path"]} for c in contents]
        )
    
    def query(self, query: str) -> str:
        docs = self.db.similarity_search(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        
        llm = OpenAI(api_key=settings.OPENAI_API_KEY)
        return llm.invoke(
            f"Context about the repository:\n{context}\n\nQuestion: {query}"
        )
