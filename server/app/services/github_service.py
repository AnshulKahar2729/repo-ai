from github import Github
from app.core.config import settings
from app.utils.url_parser import parse_github_url
from typing import List, Dict
from langchain.vectorstores import FAISS
from github import Github
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


class GitHubService:
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
        self.github_client = Github(GITHUB_TOKEN)
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.llm = ChatOpenAI(temperature=0)
    
    def get_repo_contents(self, repo_url: str) -> List[Dict[str, str]]:
        owner, repo_name = parse_github_url(repo_url)
        print(f"Owner: {owner}, Repo: {repo_name}")
        repo = self.client.get_repo(f"{owner}/{repo_name}")
        print(f"Repo: {repo}")
        return self._traverse_contents(repo, "")
    
    def _traverse_contents(self, repo, path: str) -> List[Dict[str, str]]:
        contents = []
        
        try:
            for content in repo.get_contents(path):
                if content.type == "file":
                    contents.append({
                        "path": content.path,
                        "content": content.decoded_content.decode('utf-8')
                    })
                elif content.type == "dir":
                    dir_contents = self._traverse_contents(repo, content.path)
                    contents.extend(dir_contents)
        except Exception as e:
            print(f"Error accessing {path}: {str(e)}")
        print(f"Contents: {contents}")
        return contents
    
    async def answer_question(self, repo_id: str, question: str):
        vectorstore = FAISS.load_local(
            f"vectorstores/{repo_id}", 
            self.embeddings
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
        )
        return await qa_chain.arun(question)

    def _create_vectorstore(self, contents):
        chunks = []
        for doc in contents:
            file_chunks = self.text_splitter.split_text(doc["content"])
            chunks.extend([{
                "text": chunk,
                "metadata": doc["metadata"]
            } for chunk in file_chunks])
            
        vectorstore = FAISS.from_texts(
            texts=[c["text"] for c in chunks],
            embedding=self.embeddings,
            metadatas=[c["metadata"] for c in chunks]
        )
        
        # Save locally
        vectorstore.save_local(f"vectorstores/{repo_id}")
        return vectorstore

    async def process_repo(self, repo_url):
        repo = self.client.get_repo(self._parse_repo_url(repo_url))
        contents = []
        
        for file in repo.get_contents(""):
            if file.type == "file" and self._is_valid_file(file.name):
                content = file.decoded_content.decode()
                contents.append({
                    "content": content,
                    "metadata": {"path": file.path}
                })

        return self._create_vectorstore(contents)

