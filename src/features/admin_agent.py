# src/features/admin_agent.py


class AdminAgent:
    def schedule_appointment(self, patient_name: str, date: str) -> str:
        # Lógica para agendar citas
        return f"Cita agendada para {patient_name} el {date}."

    def manage_patient_records(self, patient_name: str, action: str) -> str:
        # Nueva función para manejar registros de pacientes
        return f"Se ha {action} el registro de {patient_name}."