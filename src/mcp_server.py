from mcp.server.fastmcp import FastMCP
from ai_analyzer import AIAnalyzer

mcp = FastMCP(
    "AI Incident Resolution Assistant"
)

analyzer = AIAnalyzer()


@mcp.tool()
async def analyze_incident(
    log_content: str,
    log_type: str = "GENERAL"
):
    """
    Analyze incident logs and identify root cause.
    """

    result = await analyzer.analyze_incident(
        log_content=log_content,
        log_type=log_type
    )

    return result


if __name__ == "__main__":
    mcp.run()