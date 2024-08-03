# src/features/patient_rag.py

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document


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
                    documents.append(Document(page_content=content, metadata={"source": filename}))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        return Chroma.from_documents(splits, self.embeddings)

    def query(self, question: str) -> str:
        if question.lower().startswith("paciente"):
            file_name = f"{question.lower()}.txt"
            file_path = os.path.join(self.patients_directory, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return f"Información del {question}:\n{file.read()}"

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