# src/models/input_models.py


from pydantic import BaseModel, Field

class DiagnoseInput(BaseModel):
    symptoms: str = Field(description="Síntomas del paciente")

class CheckVitalsInput(BaseModel):
    patient_name: str = Field(description="Nombre del paciente")

class ScheduleAppointmentInput(BaseModel):
    patient_name: str = Field(description="Nombre del paciente")
    date: str = Field(description="Fecha de la cita")

class QueryInput(BaseModel):
    question: str = Field(description="Pregunta sobre el paciente")