import os

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.logger_config import get_logger
from src.ai_analyzer import AIAnalyzer
from src.github_integration import GitHubIntegration
from src.agent_orchestrator import AgentOrchestrator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger()
logger.info("Starting AI Incident Resolution Assistant")

analyzer = AIAnalyzer()
orchestrator = AgentOrchestrator()
github_client = GitHubIntegration()


class IncidentRequest(BaseModel):
    error_message: str
    log_type: str = "GENERAL"
    create_github_issue: bool = False


@app.get("/health")
async def health_check():
    logger.info("Health check called")

    return {
        "status": "UP",
        "service": "AI Incident Resolution Assistant"
    }


@app.post("/analyze/manual")
async def analyze_incident(request: IncidentRequest):
    logger.info("Manual incident analysis started")

    result = await analyzer.analyze_incident(
        log_content=request.error_message,
        log_type=request.log_type
    )

    if request.create_github_issue:
        logger.info("Creating GitHub issue")
        github_url = github_client.create_issue(result)
        result["github_issue_url"] = github_url

    logger.info("Manual incident analysis completed")

    return result


@app.post("/analyze/upload")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    logger.info(f"Processing uploaded file: {file.filename}")

    content = await file.read()
    log_text = content.decode("utf-8")

    result = await analyzer.analyze_incident(
        log_content=log_text,
        log_type="FILE"
    )

    logger.info("Creating GitHub issue from uploaded file")
    github_url = github_client.create_issue(result)
    result["github_issue_url"] = github_url

    logger.info("File incident analysis completed")

    return result


@app.post("/orchestrate/analyze")
async def orchestrate_analysis(request: IncidentRequest):
    logger.info("ICA agentic orchestration started")

    result = await orchestrator.run_incident_flow(
        incident_text=request.error_message,
        source="manual_or_auto_input"
    )

    logger.info("ICA agentic orchestration completed")

    return result


@app.get("/watch/latest")
async def watch_latest_file():
    folder_path = "logs/incoming"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".log") or f.lower().endswith(".txt")
    ]

    if not files:
        return {
            "found": False,
            "filename": "",
            "content": ""
        }

    latest_file = max(files, key=os.path.getmtime)

    with open(latest_file, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    return {
        "found": True,
        "filename": os.path.basename(latest_file),
        "content": content
    }