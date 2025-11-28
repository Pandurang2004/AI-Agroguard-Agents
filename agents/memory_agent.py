# agents/memory_agent.py

from core import memory_store

class MemoryAgent:
    def add_case(self, farmer_id: str, crop: str, location: str,
                 diagnosis: str, recommendation: str, risk_level: str = "Unknown"):
        memory_store.add_entry(
            farmer_id=farmer_id,
            crop=crop,
            location=location,
            diagnosis=diagnosis,
            recommendation=recommendation,
            risk_level=risk_level
        )

    def get_history(self, farmer_id: str):
        return memory_store.get_history(farmer_id)
