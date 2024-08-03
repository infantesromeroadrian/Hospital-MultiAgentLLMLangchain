# src/features/hospital_tools.py

from langchain.tools import StructuredTool
from features.patient_rag import PatientRAG
from features.doctor_agent import DoctorAgent
from features.nurse_agent import NurseAgent
from features.admin_agent import AdminAgent
from models.input_models import DiagnoseInput, CheckVitalsInput, ScheduleAppointmentInput, QueryInput, TreatmentInput, MedicationInput, RecordActionInput
import os

class HospitalTools:
    def __init__(self, rag_system: PatientRAG):
        self.rag_system = rag_system
        self.doctor = DoctorAgent()
        self.nurse = NurseAgent()
        self.admin = AdminAgent()

    def list_patients(self) -> str:
        return ', '.join([f.split('.')[0] for f in os.listdir(self.rag_system.patients_directory) if f.endswith('.txt')])

    def get_tools(self):
        return [
            StructuredTool.from_function(
                func=self.rag_system.query,
                name="consulta_paciente",
                description="Útil para buscar información específica sobre un paciente.",
                args_schema=QueryInput
            ),
            StructuredTool.from_function(
                func=self.doctor.diagnose,
                name="diagnostico",
                description="Útil para obtener un diagnóstico preliminar basado en síntomas.",
                args_schema=DiagnoseInput
            ),
            StructuredTool.from_function(
                func=self.doctor.recommend_treatment,
                name="recomendar_tratamiento",
                description="Útil para recomendar un tratamiento basado en un diagnóstico.",
                args_schema=TreatmentInput
            ),
            StructuredTool.from_function(
                func=self.nurse.check_vitals,
                name="verificar_signos_vitales",
                description="Útil para verificar los signos vitales de un paciente.",
                args_schema=CheckVitalsInput
            ),
            StructuredTool.from_function(
                func=self.nurse.administer_medication,
                name="administrar_medicacion",
                description="Útil para administrar medicación a un paciente.",
                args_schema=MedicationInput
            ),
            StructuredTool.from_function(
                func=self.admin.schedule_appointment,
                name="agendar_cita",
                description="Útil para agendar una cita para un paciente.",
                args_schema=ScheduleAppointmentInput
            ),
            StructuredTool.from_function(
                func=self.admin.manage_patient_records,
                name="manejar_registros",
                description="Útil para manejar los registros de un paciente.",
                args_schema=RecordActionInput
            ),
            StructuredTool.from_function(
                func=self.list_patients,
                name="listar_pacientes",
                description="Útil para obtener una lista de todos los pacientes disponibles."
            )
        ]