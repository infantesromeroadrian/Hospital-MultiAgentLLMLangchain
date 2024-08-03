# src/features/admin_agent.py


class AdminAgent:
    def schedule_appointment(self, patient_name: str, date: str) -> str:
        return f"Cita agendada para {patient_name} el {date}."