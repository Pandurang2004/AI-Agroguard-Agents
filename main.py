# main.py

from core.models import LLMClient
from agents.diagnosis_agent import DiagnosisAgent
from agents.recommendation_agent import RecommendationAgent
from agents.weather_risk_agent import WeatherRiskAgent
from agents.memory_agent import MemoryAgent
from agents.report_agent import ReportAgent

from rich import print


def main():
    print("[bold green]AI AgroGuard - Multi-Agent Pest & Crop Health Copilot[/bold green]\n")

    farmer_id = input("Farmer ID (any string, e.g. phone number): ").strip()
    crop = input("Crop name (e.g. Tomato, Cotton): ").strip()
    location = input("Location (City/District, State): ").strip()
    symptoms = input("Describe the symptoms you see (spots, color, insects, etc.): ").strip()

    llm = LLMClient()

    diagnosis_agent = DiagnosisAgent(llm)
    recommendation_agent = RecommendationAgent(llm)
    weather_agent = WeatherRiskAgent(llm)
    memory_agent = MemoryAgent()
    report_agent = ReportAgent(llm, memory_agent)

    print("\n[bold]Running Diagnosis Agent...[/bold]")
    diagnosis = diagnosis_agent.run(crop, symptoms)
    print("\n[cyan]Diagnosis Result:[/cyan]\n", diagnosis)

    print("\n[bold]Running Recommendation Agent...[/bold]")
    recommendation = recommendation_agent.run(crop, diagnosis)
    print("\n[cyan]Recommendation:[/cyan]\n", recommendation)

    print("\n[bold]Running Weather & Risk Agent (Tool)...[/bold]")
    risk_analysis, weather = weather_agent.run(crop, location, diagnosis)
    print("\n[cyan]Weather-based Risk Analysis:[/cyan]\n", risk_analysis)
    print("\n[cyan]Weather Data Used:[/cyan]\n", weather)

    # Simple placeholder risk level extraction
    guessed_risk_level = "High" if "High" in risk_analysis else "Medium" if "Medium" in risk_analysis else "Low"

    # Store in memory
    memory_agent.add_case(
        farmer_id=farmer_id,
        crop=crop,
        location=location,
        diagnosis=diagnosis,
        recommendation=recommendation,
        risk_level=guessed_risk_level
    )

    print("\n[bold]Generating Weekly-style Report (Report Agent)...[/bold]")
    report = report_agent.run(farmer_id)
    print("\n[magenta]Weekly Report:[/magenta]\n", report)

    print("\n[bold green]Pipeline completed successfully.[/bold green]")


if __name__ == "__main__":
    main()
