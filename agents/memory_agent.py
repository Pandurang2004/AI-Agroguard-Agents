# agents/memory_agent.py

from typing import List, Dict, Any
from collections import Counter
from core import memory_store


class MemoryAgent:
    def add_case(
        self,
        farmer_id: str,
        crop: str,
        location: str,
        diagnosis: str,
        recommendation: str,
        risk_level: str = "Unknown",
    ) -> None:
        memory_store.add_entry(
            farmer_id=farmer_id,
            crop=crop,
            location=location,
            diagnosis=diagnosis,
            recommendation=recommendation,
            risk_level=risk_level,
        )

    def get_history(self, farmer_id: str) -> List[Dict[str, Any]]:
        return memory_store.get_history(farmer_id)

    def get_all_cases(self) -> List[Dict[str, Any]]:
        return memory_store.get_all_entries()

    def find_similar_cases(self, crop: str, location: str) -> List[Dict[str, Any]]:
        return memory_store.find_similar_entries(crop, location)

    # ---------- AUTO-LEARNING SUPPORT HELPERS ----------

    def summarize_farmer_trends(self, farmer_id: str) -> str:
        history = self.get_history(farmer_id)
        if not history:
            return "No prior data for this farmer."

        crops = [h["crop"] for h in history]
        risks = [h["risk_level"] for h in history]
        diagnoses = [h["diagnosis"][:60] for h in history]

        crop_summary = ", ".join([f"{c}: {n} times" for c, n in Counter(crops).items()])
        risk_summary = ", ".join([f"{r}: {n}" for r, n in Counter(risks).items()])
        recent_diag = "; ".join(diagnoses[-3:])

        return (
            f"Crop usage history: {crop_summary}.\n"
            f"Risk trend: {risk_summary}.\n"
            f"Recent diagnosis snippets: {recent_diag}."
        )

    def summarize_local_trends(self, crop: str, location: str) -> str:
        similar = self.find_similar_cases(crop, location)
        if not similar:
            return f"No prior cases for crop {crop} at {location}."

        risk_counts = Counter([s["risk_level"] for s in similar])
        risk_summary = ", ".join([f"{r}: {n}" for r, n in risk_counts.items()])

        return (
            f"There are {len(similar)} previous cases for crop {crop} at {location}. "
            f"Risk distribution: {risk_summary}."
        )
