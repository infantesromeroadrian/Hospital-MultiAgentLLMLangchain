# src/models/input_models.py

from pydantic import BaseModel, Field

class DiagnoseInput(BaseModel):
    symptoms: str = Field(description="Síntomas del paciente")

class TreatmentInput(BaseModel):
    diagnosis: str = Field(description="Diagnóstico del paciente")

class CheckVitalsInput(BaseModel):
    patient_name: str = Field(description="Nombre del paciente")

class MedicationInput(BaseModel):
    patient_name: str = Field(description="Nombre del paciente")
    medication: str = Field(description="Medicación a administrar")

class ScheduleAppointmentInput(BaseModel):
    patient_name: str = Field(description="Nombre del paciente")
    date: str = Field(description="Fecha de la cita")

class RecordActionInput(BaseModel):
    patient_name: str = Field(description="Nombre del paciente")
    action: str = Field(description="Acción a realizar en el registro")

class QueryInput(BaseModel):
    question: str = Field(description="Pregunta sobre el paciente")