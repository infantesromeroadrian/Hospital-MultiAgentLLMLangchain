# streamlit run src/app.py

import streamlit as st
import os
from dotenv import load_dotenv
from features.patient_rag import PatientRAG
from features.hospital_tools import HospitalTools
from agents.hospital_agent import HospitalAgent
from utils.logging_config import setup_logging
import logging

load_dotenv()
setup_logging()


class StreamlitHospitalApp:
    def __init__(self, patients_directory: str):
        self.patients_directory = patients_directory
        self.rag_system = PatientRAG(patients_directory)
        hospital_tools = HospitalTools(self.rag_system)
        self.agent = HospitalAgent(hospital_tools.get_tools())

    def run(self):
        st.title("Sistema de Consulta de Pacientes del Hospital")

        # Autenticación básica
        user_type = st.sidebar.selectbox("Seleccione tipo de usuario", ["Doctor", "Paciente"])
        if user_type == "Doctor":
            password = st.sidebar.text_input("Contraseña", type="password", key="doctor_password")
            if password != "doctor123":  # Esto es solo un ejemplo, en un sistema real usarías una autenticación más segura
                st.sidebar.error("Contraseña incorrecta")
                return

        if user_type == "Doctor":
            self.doctor_interface()
        else:
            self.patient_interface()

    def doctor_interface(self):
        st.header("Interfaz de Doctor")

        query = st.text_input("Consulta sobre paciente:")
        if st.button("Enviar consulta"):
            if query:
                try:
                    response = self.agent.run(query)
                    st.write("Respuesta:")
                    st.write(response['output'])
                    st.write(f"Herramienta utilizada: {response['tool_used']}")
                except Exception as e:
                    st.error(f"Ocurrió un error: {str(e)}")

        st.subheader("Añadir comentario a paciente")
        patient_name = st.text_input("Nombre del paciente:")
        comment = st.text_area("Comentario:")
        if st.button("Añadir comentario"):
            if patient_name and comment:
                self.add_comment_to_patient(patient_name, comment)
                st.success("Comentario añadido con éxito")
            else:
                st.warning("Por favor, complete todos los campos")

    def patient_interface(self):
        st.header("Interfaz de Paciente")

        patient_name = st.text_input("Su nombre:", key="patient_name_input")

        if 'patient_data' not in st.session_state:
            st.session_state.patient_data = {
                "name": "",
                "age": "",
                "gender": "",
                "condition": "",
                "medication": "",
                "reason": ""
            }

        if patient_name:
            st.session_state.patient_data["name"] = patient_name

            st.session_state.patient_data["age"] = st.text_input("¿Cuál es su edad?",
                                                                 st.session_state.patient_data["age"], key="age_input")
            st.session_state.patient_data["gender"] = st.text_input("¿Cuál es su género?",
                                                                    st.session_state.patient_data["gender"],
                                                                    key="gender_input")
            st.session_state.patient_data["condition"] = st.text_input("¿Tiene alguna condición médica preexistente?",
                                                                       st.session_state.patient_data["condition"],
                                                                       key="condition_input")
            st.session_state.patient_data["medication"] = st.text_input("¿Está tomando algún medicamento actualmente?",
                                                                        st.session_state.patient_data["medication"],
                                                                        key="medication_input")
            st.session_state.patient_data["reason"] = st.text_input("¿Cuál es el motivo de su visita hoy?",
                                                                    st.session_state.patient_data["reason"],
                                                                    key="reason_input")

            if st.button("Guardar registro", key="save_button"):
                self.create_new_patient_record(st.session_state.patient_data)
                st.success(f"Registro creado para {patient_name}")
                st.session_state.patient_data = {key: "" for key in st.session_state.patient_data}  # Reset the form


    def add_comment_to_patient(self, patient_name: str, comment: str):
        file_name = f"{patient_name.lower()}.txt"
        file_path = os.path.join(self.patients_directory, file_name)
        with open(file_path, 'a') as file:
            file.write(f"\nComentario del doctor: {comment}\n")

        # Actualizar el vector store
        self.rag_system.update_patient_data(patient_name)

    def create_new_patient_record(self, patient_data):
        file_name = f"{patient_data['name'].lower()}.txt"
        file_path = os.path.join(self.patients_directory, file_name)

        with open(file_path, 'w') as file:
            for key, value in patient_data.items():
                file.write(f"{key.capitalize()}: {value}\n")


        questions = [
            "¿Cuál es su edad?",
            "¿Cuál es su género?",
            "¿Tiene alguna condición médica preexistente?",
            "¿Está tomando algún medicamento actualmente?",
            "¿Cuál es el motivo de su visita hoy?"
        ]

        answers = []
        for question in questions:
            answer = st.text_input(question)
            answers.append(answer)

        if st.button("Guardar registro"):
            with open(file_path, 'w') as file:
                file.write(f"Paciente: {patient_data['name']}\n\n")
                for q, a in zip(questions, answers):
                    file.write(f"{q}\n{a}\n\n")

            # Actualizar el vector store
            self.rag_system.update_patient_data(patient_data['name'])
            st.success(f"Registro creado para {patient_data['name']}")


if __name__ == "__main__":
    app = StreamlitHospitalApp("../data/pacientes")
    app.run()