# 🌾 AI AgroGuard – Multi-Agent Crop Health & Pest Risk Copilot

AI AgroGuard is a **multi-agent AI system** that helps small and rural farmers diagnose crop issues, get localized treatment guidance, and understand weather-driven risk — in **their own language**.

It combines:
- 👨‍🌾 a simple Streamlit UI for farmers,
- 🤖 multiple LLM-powered agents (diagnosis, recommendation, weather risk, reporting),
- 🌦 real weather tools,
- 🧠 memory & auto-learning over time.

> Built as part of the **Agents Intensive – Capstone Project (Kaggle x Google)**.

---

## 🌱 Problem

Small and rural farmers often struggle with:

- Identifying **pests and diseases** early.
- Getting **trusted, localized advice** instead of random YouTube / WhatsApp tips.
- Understanding **weather-driven risk** (humidity, rain → higher disease pressure).
- Having **continuous history** of their farm health across weeks.

Most advisory systems are:
- Single-shot (no memory),
- English-only,
- Not tailored to the farmer’s past issues.

---

## ✅ Solution – AI AgroGuard

AI AgroGuard is a **multi-agent crop health assistant** that:

1. **Diagnoses crop problems** from farmer’s description (and optionally images via Gemini Vision).
2. **Generates treatment plans** with both chemical and organic options.
3. **Analyzes live weather data** (via Open-Meteo API) to assess disease risk.
4. **Learns from farmer history** over time to adapt recommendations.
5. **Supports multiple languages**: English, Hindi, Marathi, Kannada.
6. **Stores & visualizes history** per farmer as a case history table and weekly report.

---

## 🧠 Key Features (mapped to Capstone rubric)

### 1. Multi-Agent System
- `DiagnosisAgent` – identifies likely disease/pest from symptoms (+ image-aware).
- `RecommendationAgent` – gives treatment & prevention plan, **auto-learning from history**.
- `WeatherRiskAgent` – uses **weather tool** to compute risk based on humidity, rain, temperature.
- `MemoryAgent` – stores and retrieves farmer cases in a JSON-backed “memory store”.
- `ReportAgent` – generates **weekly health reports** for each farmer.

### 2. Tools & External Integrations
- **LLM Tool**  
  - `LLMClient` wrapper over **Gemini** (text + vision capable).
- **Weather Tool**  
  - `core/tools.py` calls **Open-Meteo** APIs for geocoding + hourly weather forecasts.
- **Persistence Tool (Memory)**  
  - `core/memory_store.py` stores all past cases in `farmer_memory.json`.

### 3. Memory & Auto-Learning
- Per-farmer history is stored with:
  - `farmer_id`, `crop`, `location`, `diagnosis`, `recommendation`, `risk_level`, `timestamp`.
- `MemoryAgent` exposes:
  - `get_history(farmer_id)` – farmer’s own cases.
  - `find_similar_cases(crop, location)` – local patterns.
  - `summarize_farmer_trends(...)` – repeated crops, risk trends, repeated diseases.
  - `summarize_local_trends(...)` – risk distribution for that crop+location.

- `RecommendationAgent` uses these summaries to:
  - Strengthen advice for farmers with many **High risk** events.
  - Suggest crop rotation / resistant varieties for **repeated diseases**.
  - Warn if **this region** (crop+location) appears frequently in the data.
  - Encourage farmers when trends are improving.

### 4. Multilingual Support (Rural-Farmer-friendly)
The app supports:
- **English**
- **हिंदी (Hindi)**
- **मराठी (Marathi)**
- **ಕನ್ನಡ (Kannada)**

Language selection in the UI:
- Affects **diagnosis**, **treatment recommendations**, and **weekly reports**.
- Prompts instruct Gemini to respond in the selected language using simple, short sentences suitable for small farmers.

---

## 🧩 System Architecture

### High-Level Flow

1. Farmer opens **Streamlit app**.
2. Inputs:
   - Farmer ID (phone/ID)
   - Crop
   - Location
   - Symptoms (text)
   - Optional leaf image
   - Preferred language
3. System runs:
   - `DiagnosisAgent` → disease / pest guess.
   - `WeatherRiskAgent` → risk score using weather API.
   - `MemoryAgent` → fetch history & trend summaries.
   - `RecommendationAgent` → personalized treatment.
   - `ReportAgent` → weekly summary.
4. Results:
   - Diagnosis card
   - Weather risk card (color-coded)
   - Treatment & recommendations card
   - Weekly report card
   - Farmer-specific **Case history table**

---

## 🏗 Architecture Diagram (Mermaid)

You can embed this in your docs, or render it into an image for Kaggle:

```mermaid
flowchart LR

    subgraph UI["🖥️ Streamlit Web UI"]
        A[Farmer Inputs\nID, Crop, Location, Symptoms, Image, Language]
        B[Results Dashboard\nDiagnosis, Risk, Plan, History]
    end

    subgraph Orchestrator["🧠 Orchestrator (app.py)"]
        O1[Run Pipeline]
    end

    subgraph Agents["🤖 Multi-Agent Layer"]
        D[DiagnosisAgent]
        R[RecommendationAgent]
        W[WeatherRiskAgent]
        M[MemoryAgent]
        RP[ReportAgent]
    end

    subgraph LLM["✨ LLM & Vision"]
        L[LLMClient\n(Gemini)]
    end

    subgraph Tools["🛠 External Tools"]
        T1[Weather Tool\ncore/tools.py\nOpen-Meteo API]
        T2[Memory Store\ncore/memory_store.py\nfarmer_memory.json]
    end

    A --> O1
    O1 --> D
    O1 --> W
    O1 --> M
    O1 --> R
    O1 --> RP

    D --> L
    R --> L
    RP --> L

    W --> T1
    M --> T2

    M --> R
    M --> RP

    O1 --> B
