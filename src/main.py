import os
from dotenv import load_dotenv
from src.features.patient_rag import PatientRAG
from src.features.hospital_tools import HospitalTools
from src.agents.hospital_agent import HospitalAgent
from src.utils.logging_config import setup_logging
import logging

load_dotenv()
setup_logging()

class HospitalApplication:
    def __init__(self, patients_directory: str):
        self.patients_directory = patients_directory
        rag_system = PatientRAG(patients_directory)
        hospital_tools = HospitalTools(rag_system)
        self.agent = HospitalAgent(hospital_tools.get_tools())

    def run_interaction(self):
        print("Bienvenido al Sistema de Consulta de Pacientes del Hospital")
        while True:
            query = input("\nPor favor, ingrese su consulta (o 'salir' para terminar): ")
            if query.lower() == 'salir':
                print("Gracias por usar el Sistema de Consulta de Pacientes del Hospital. ¡Hasta luego!")
                break
            try:
                logging.info(f"Consulta recibida: {query}")
                response = self.agent.run(query)
                logging.info(f"Respuesta generada: {response['output']}")
                logging.info(f"Herramienta utilizada: {response['tool_used']}")
                print("\nRespuesta:", response['output'])
                print(f"Herramienta utilizada: {response['tool_used']}")
            except Exception as e:
                logging.error(f"Error ocurrido: {str(e)}")
                print(f"\nOcurrió un error: {str(e)}")
                print("Por favor, intente reformular su consulta.")

if __name__ == "__main__":
    app = HospitalApplication("../data/pacientes")
    app.run_interaction()