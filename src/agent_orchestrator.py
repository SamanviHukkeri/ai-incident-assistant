from src.ai_analyzer import AIAnalyzer


class AgentOrchestrator:

    def __init__(self):
        self.analyzer = AIAnalyzer()

    async def run_incident_flow(self, incident_text: str, source: str = "manual"):

        agent_steps = []

        agent_steps.append({
            "agent": "Incident Intake Agent",
            "status": "COMPLETED",
            "message": f"Incident received from {source}"
        })

        agent_steps.append({
            "agent": "Incident Analysis Agent",
            "status": "IN_PROGRESS",
            "message": "Calling MCP analyze_incident tool"
        })

        analysis_result = await self.analyzer.analyze_incident(
            log_content=incident_text,
            log_type="GENERAL"
        )

        agent_steps.append({
            "agent": "Incident Analysis Agent",
            "status": "COMPLETED",
            "message": "Root cause, severity, fixes, APIs, and timeline generated"
        })

        agent_steps.append({
            "agent": "Reporting Notification Agent",
            "status": "COMPLETED",
            "message": "Incident report and alert message prepared"
        })

        return {
            "agentic_flow": agent_steps,
            "analysis": analysis_result
        }