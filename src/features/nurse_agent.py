# src/features/nurse_agent.py


class NurseAgent:
    def check_vitals(self, patient_name: str) -> str:
        # Lógica para verificar signos vitales
        return f"Los signos vitales de {patient_name} son normales."

    def administer_medication(self, patient_name: str, medication: str) -> str:
        # Nueva función para administrar medicación
        return f"Se ha administrado {medication} a {patient_name} según lo prescrito."