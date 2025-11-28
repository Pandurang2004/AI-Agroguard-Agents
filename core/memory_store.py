# core/memory_store.py

import json
import os
from datetime import datetime
from typing import List, Dict, Any

MEMORY_FILE = "farmer_memory.json"


def _load_memory() -> List[Dict[str, Any]]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_memory(entries: List[Dict[str, Any]]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def add_entry(farmer_id: str, crop: str, location: str,
              diagnosis: str, recommendation: str, risk_level: str) -> None:
    entries = _load_memory()
    entries.append({
        "farmer_id": farmer_id,
        "timestamp": datetime.utcnow().isoformat(),
        "crop": crop,
        "location": location,
        "diagnosis": diagnosis,
        "recommendation": recommendation,
        "risk_level": risk_level
    })
    _save_memory(entries)


def get_history(farmer_id: str) -> List[Dict[str, Any]]:
    entries = _load_memory()
    return [e for e in entries if e["farmer_id"] == farmer_id]
