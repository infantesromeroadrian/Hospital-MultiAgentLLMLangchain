# streamlit run src/app.py

import streamlit as st
import os
from dotenv import load_dotenv
from features.patient_rag import PatientRAG
from features.hospital_tools import HospitalTools
from agents.hospital_agent import HospitalAgent
from utils.logging_config import setup_logging
import logging

# Ensure the working directory is set correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
setup_logging()


class StreamlitHospitalApp:
    def __init__(self, patients_directory: str):
        self.patients_directory = patients_directory
        rag_system = PatientRAG(patients_directory)
        hospital_tools = HospitalTools(rag_system)
        self.agent = HospitalAgent(hospital_tools.get_tools())

    def run(self):
        st.title("Sistema de Consulta de Pacientes del Hospital")

        query = st.text_input("Por favor, ingrese su consulta:")

        if st.button("Enviar consulta"):
            if query:
                try:
                    logging.info(f"Consulta recibida: {query}")
                    response = self.agent.run(query)
                    logging.info(f"Respuesta generada: {response['output']}")
                    logging.info(f"Herramienta utilizada: {response['tool_used']}")

                    st.write("Respuesta:")
                    st.write(response['output'])
                    st.write(f"Herramienta utilizada: {response['tool_used']}")
                except Exception as e:
                    logging.error(f"Error ocurrido: {str(e)}")
                    st.error(f"Ocurrió un error: {str(e)}")
                    st.write("Por favor, intente reformular su consulta.")
            else:
                st.warning("Por favor, ingrese una consulta.")

        st.sidebar.title("Información")
        st.sidebar.info("Este es un sistema de consulta de pacientes del hospital. "
                        "Puede hacer preguntas sobre pacientes, agendar citas, "
                        "verificar signos vitales y más.")

        if st.sidebar.button("Listar Pacientes"):
            patients = self.agent.run("listar pacientes")
            st.sidebar.write(patients['output'])


if __name__ == "__main__":
    app = StreamlitHospitalApp("../data/pacientes")
    app.run()