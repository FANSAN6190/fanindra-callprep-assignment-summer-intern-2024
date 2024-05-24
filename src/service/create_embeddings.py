from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import os
from pdfminer.high_level import extract_text


class create_embeddings:
    def __init__(self):
        self.pc = Pinecone(api_key='a8861bb3-e7fa-469d-aecf-0372fbed64ee')
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
            text = extract_text(doc_path)
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