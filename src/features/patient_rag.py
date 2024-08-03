# src/features/patient_rag.py

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
import unicodedata
from fuzzywuzzy import fuzz
import numpy as np


class PatientRAG:
    def __init__(self, patients_directory: str):
        self.patients_directory = patients_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self.load_patient_data()

    def load_patient_data(self):
        documents = []
        for filename in os.listdir(self.patients_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.patients_directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    normalized_name = self.normalize_name(filename.split('.')[0])
                    documents.append(Document(page_content=content,
                                              metadata={"source": filename, "normalized_name": normalized_name}))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        return Chroma.from_documents(splits, self.embeddings)

    def normalize_name(self, name: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', name.lower())
                       if unicodedata.category(c) != 'Mn')

    def find_best_match(self, query: str, threshold: int = 80) -> str:
        normalized_query = self.normalize_name(query)
        all_docs = self.vector_store.get()
        best_match = None
        best_score = 0
        for doc in all_docs['metadatas']:
            score = fuzz.ratio(normalized_query, doc['normalized_name'])
            if score > best_score and score >= threshold:
                best_score = score
                best_match = doc['source']
        return best_match

    def query(self, question: str) -> str:
        best_match = self.find_best_match(question)
        if best_match:
            file_path = os.path.join(self.patients_directory, best_match)
            with open(file_path, 'r', encoding='utf-8') as file:
                return f"Información del paciente {best_match.split('.')[0]}:\n{file.read()}"

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(temperature=0, model_name="gpt-4"),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        result = qa_chain({"query": question})

        if not result['result']:
            return f"No se encontró información para la consulta: {question}"

        return f"Respuesta: {result['result']}\nFuentes: {[doc.metadata['source'] for doc in result['source_documents']]}"

    def update_patient_data(self, patient_name: str):
        file_name = f"{patient_name.lower()}.txt"
        file_path = os.path.join(self.patients_directory, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            normalized_name = self.normalize_name(patient_name)
            document = Document(page_content=content,
                                metadata={"source": file_name, "normalized_name": normalized_name})

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents([document])

        # Intentar obtener documentos existentes
        existing_docs = self.vector_store.get(where={"source": file_name})

        if existing_docs and len(existing_docs['ids']) > 0:
            # Si existen documentos, eliminarlos
            self.vector_store.delete(ids=existing_docs['ids'])

        # Añadir los nuevos documentos
        self.vector_store.add_documents(splits)

        print(f"Datos actualizados para el paciente {patient_name}")

    def list_patients(self) -> List[str]:
        return [f.split('.')[0] for f in os.listdir(self.patients_directory) if f.endswith('.txt')]