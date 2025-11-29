import streamlit as st
from core.models import LLMClient
from agents.diagnosis_agent import DiagnosisAgent
from agents.recommendation_agent import RecommendationAgent
from agents.weather_risk_agent import WeatherRiskAgent
from agents.memory_agent import MemoryAgent
from agents.report_agent import ReportAgent

st.set_page_config(page_title="AI AgroGuard", layout="wide")


# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.card {
    background: rgba(255,255,255,0.07);
    padding: 18px 25px;
    border-radius: 14px;
    box-shadow: 0px 0px 12px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
    margin-bottom: 18px;
}

.sidebar .sidebar-content {
    background-color: #1c1e24 !important;
}

.block-container {
    padding-top: 1.2rem;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center; color:#90ee90;'>🌾 AI AgroGuard</h1>
<h4 style='text-align: center; color:#cccccc;'>Intelligent Crop Disease, Treatment & Weather Risk Advisor</h4>
<hr style='border:1px solid #444;'/>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR FORM ----------------
st.sidebar.header("🧑‍🌾 Farmer Information")
farmer_id = st.sidebar.text_input("Farmer ID (e.g. 101)")
crop = st.sidebar.text_input("Crop Name (e.g. Tomato, Cotton)")
location = st.sidebar.text_input("Location (City, State)")
symptoms = st.sidebar.text_area("Describe Visible Symptoms")
run_button = st.sidebar.button("🚀 Run AgroGuard System")


# Initialize memory
memory_agent = MemoryAgent()


# ---------------- MAIN PIPELINE ----------------
if run_button:
    if not farmer_id or not crop or not location or not symptoms:
        st.error("⚠ Please complete all fields before running the system.")
    else:
        st.info("⏳ Running intelligent multi-agent pipeline...")

        llm = LLMClient()
        diagnosis_agent = DiagnosisAgent(llm)
        recommendation_agent = RecommendationAgent(llm)
        weather_agent = WeatherRiskAgent(llm)
        report_agent = ReportAgent(llm, memory_agent)

        diagnosis = diagnosis_agent.run(crop, symptoms)
        recommendation = recommendation_agent.run(crop, diagnosis)
        risk_analysis, weather = weather_agent.run(crop, location, diagnosis)

        guessed_risk = "High" if "High" in risk_analysis else "Medium" if "Medium" in risk_analysis else "Low"

        memory_agent.add_case(
            farmer_id=farmer_id,
            crop=crop,
            location=location,
            diagnosis=diagnosis,
            recommendation=recommendation,
            risk_level=guessed_risk
        )

        report = report_agent.run(farmer_id)


        # --------------- UI LAYOUT ---------------
        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown("### 🧪 Diagnosis Result")
            st.markdown(f"<div class='card'>{diagnosis}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("### 🌧 Weather Risk Analysis")

            risk_style = {
                "High": "background-color:#ff4d4d;color:white;",
                "Medium": "background-color:#ffeb3b;color:black;",
                "Low": "background-color:#4CAF50;color:white;"
            }

            st.markdown(
                f"<div style='padding:10px;border-radius:10px;font-size:19px;text-align:center;{risk_style[guessed_risk]}'>"
                f"🚨 Crop Risk Level: <b>{guessed_risk}</b></div>",
                unsafe_allow_html=True
            )

            st.markdown(f"<div class='card'>{risk_analysis}</div>", unsafe_allow_html=True)

            st.markdown("### 📍 Weather Conditions Used")
            st.json(weather)


        # -------------- FULL WIDTH RECOMMENDATION BLOCK --------------
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("### 💊 Treatment & Recommendations")

        border_color = "#ff4d4d" if guessed_risk == "High" else "#ffeb3b" if guessed_risk == "Medium" else "#4CAF50"

        st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.10);
                padding: 25px 30px;
                border-left: 10px solid {border_color};
                border-radius: 16px;
                box-shadow: 0px 0px 12px rgba(0,0,0,0.35);
                backdrop-filter: blur(10px);
                font-size: 18px;
                line-height: 1.65;
                margin-top: 22px;
            ">
                <b>🌿 Recommended Action Plan</b><br><br>
                {recommendation}
            </div>
        """, unsafe_allow_html=True)


        # -------------- WEEKLY REPORT SECTION --------------
        st.markdown("### 🗓 Weekly Health Report")
        st.markdown(f"<div class='card'>{report}</div>", unsafe_allow_html=True)

        st.success("✨ Analysis Complete")


else:
    st.markdown("<h4 style='text-align:center;color:#999;'>Enter details and run system from the left panel</h4>",
                unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("""
<hr/>
<p style='text-align:center; color:#888; font-size:14px;'>
Built with ❤️ for Farmers | AI AgroGuard – Kaggle Agents Capstone 2025
</p>
""", unsafe_allow_html=True)
