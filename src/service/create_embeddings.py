from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import os
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

class CreateEmbeddings:
    def __init__(self):
        api_key = os.getenv('PINECONE_API_KEY')
        self.pc = Pinecone(api_key=api_key)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_name = 'callprep-case-studies'
        existing_indexes = self.pc.list_indexes()
        print(f"Existing indexes: {existing_indexes}")
        existing_index_names = [index['name'] for index in existing_indexes.indexes]
        print(f"Existing indexes: {existing_index_names}")
        if self.index_name not in existing_index_names:
            self.pc.create_index(
                self.index_name, 
                dimension=384,
                spec=ServerlessSpec(
                    cloud='aws', 
                    region='us-east-1'
                )
            )

        self.index = self.pc.Index(self.index_name)

    def preprocess_text(self, doc_path):
        try:
            file_extension = os.path.splitext(doc_path)[1]
            if file_extension == '.pdf':
                text = extract_text(doc_path)
            elif file_extension == '.txt':
                with open(doc_path, 'r') as f:
                    text = f.read()
            elif file_extension == '.html':
                with open(doc_path, 'r') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    text = soup.get_text()
            else:
                print(f"Unsupported file type {file_extension}")
                return ""
            return text
        except Exception as e:
            print(f"Error extracting text from {doc_path}: {e}")
            return ""

    def create_and_save_embeddings(self, doc_path, file_name):
        text = self.preprocess_text(doc_path)
        if text:
            embedding = self.model.encode(text).tolist()
            pinecone_metadata = {'filename': file_name}
            self.index.upsert([(file_name, embedding, pinecone_metadata)])
            return True
        else:
            return False
        
    def search_documents(self, query):
        query_embedding = self.model.encode(query).tolist()
        results = self.index.query(vector=query_embedding, top_k=10)
        return results
    
create_embeddings = CreateEmbeddings()