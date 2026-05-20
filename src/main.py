from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.logger_config import get_logger
from src.ai_analyzer import AIAnalyzer
from src.github_integration import GitHubIntegration

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger()

logger.info("Starting AI Incident Resolution Assistant")

# Initialize components
analyzer = AIAnalyzer()
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

    # Analyze incident
    result = await analyzer.analyze_incident(
        log_content=request.error_message,
        log_type=request.log_type
    )

    # Create GitHub issue if requested
    if request.create_github_issue:

        logger.info("Creating GitHub issue")

        github_url = github_client.create_issue(result)

        result["github_issue_url"] = github_url

    logger.info("Manual incident analysis completed")

    return result


@app.post("/analyze/upload")
async def analyze_uploaded_file(
    file: UploadFile = File(...)
):

    logger.info(f"Processing uploaded file: {file.filename}")

    # Read uploaded file
    content = await file.read()

    log_text = content.decode("utf-8")

    # Analyze logs
    result = await analyzer.analyze_incident(
        log_content=log_text,
        log_type="FILE"
    )

    # Automatically create GitHub issue
    logger.info("Creating GitHub issue from uploaded file")

    github_url = github_client.create_issue(result)

    result["github_issue_url"] = github_url

    logger.info("File incident analysis completed")

    return result