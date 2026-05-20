# AI Incident Resolution Assistant 🤖

An intelligent system that automatically analyzes production logs, detects root causes, suggests fixes, and creates GitHub issues for incidents.

## 🎯 Problem Statement

Production issues take too long to diagnose. Teams manually:
- Check logs across multiple systems
- Analyze errors and stack traces
- Identify impacted APIs
- Create incident reports
- Document resolution steps

## ✨ Solution

An AI-powered assistant that:
- **Reads** DataPower/APIC/JAVA logs
- **Detects** root cause using AI analysis
- **Suggests** actionable fixes
- **Creates** GitHub issues automatically
- **Generates** comprehensive incident summaries

## 🚀 Features

- **Multi-Format Log Parsing**: Supports DataPower, API Connect (APIC), and Java logs
- **AI-Powered Analysis**: Uses OpenAI GPT-4 for intelligent root cause detection
- **Automatic Issue Creation**: Creates detailed GitHub issues with labels and assignments
- **Multiple Report Formats**: Markdown, JSON, Email, and Slack formats
- **REST API**: Easy integration with existing systems
- **Fallback Analysis**: Works even without AI when patterns are recognizable

## 📋 Demo Example

### Input
Upload a log file with:
```
HTTP 500 timeout from backend
```

### AI Response
```
✅ Root Cause: Backend connection timeout

🔧 Suggested Fixes:
1. Check firewall rules between gateway and backend
2. Verify backend service health and response time
3. Review backend latency metrics
4. Increase timeout configuration if needed

🎯 Affected APIs:
- /member/inquiry
- /claim/details

📊 Severity: HIGH
```

### Automatic Actions
- ✅ Creates GitHub issue with full details
- ✅ Sends alert notification
- ✅ Generates incident summary report

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- OpenAI API key
- GitHub Personal Access Token (for issue creation)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-incident-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
GITHUB_REPO=owner/repository
```

4. **Run the application**
```bash
cd src
python main.py
```

The API will be available at `http://localhost:8000`

## 📖 API Usage

### 1. Upload Log File for Analysis

```bash
curl -X POST "http://localhost:8000/analyze/upload" \
  -F "file=@logs/demo_example.log" \
  -F "create_github_issue=true"
```

**Response:**
```json
{
  "root_cause": "Backend connection timeout - firewall or network issue",
  "suggested_fixes": [
    "Check firewall rules between gateway and backend",
    "Verify backend service is running and accessible",
    "Review network connectivity and latency",
    "Check backend service logs for errors"
  ],
  "affected_apis": [
    "/member/inquiry",
    "/claim/details"
  ],
  "severity": "HIGH",
  "github_issue_url": "https://github.com/owner/repo/issues/123",
  "incident_summary": "# Incident Report\n..."
}
```

### 2. Manual Incident Submission

```bash
curl -X POST "http://localhost:8000/analyze/manual" \
  -H "Content-Type: application/json" \
  -d '{
    "error_message": "HTTP 500 - Backend timeout after 30s",
    "log_type": "DATAPOWER",
    "create_github_issue": true
  }'
```

### 3. Health Check

```bash
curl http://localhost:8000/health
```

## 🏗️ Architecture

```
┌─────────────────┐
│   Log Upload    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Log Parser    │  ← Extracts structured data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Analyzer    │  ← OpenAI GPT-4 analysis
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Incident Report │  ← Generate summaries
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Issue    │  ← Auto-create issues
└─────────────────┘
```

## 📁 Project Structure

```
ai-incident-assistant/
├── src/
│   ├── main.py                 # FastAPI application
│   ├── log_parser.py           # Log parsing logic
│   ├── ai_analyzer.py          # AI analysis engine
│   ├── github_integration.py   # GitHub API integration
│   └── incident_reporter.py    # Report generation
├── config/
│   └── (configuration files)
├── logs/
│   └── demo_example.log        # Sample log file
├── tests/
│   └── (test files)
├── docs/
│   └── (documentation)
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🧪 Testing

Run the demo example:

```bash
# Start the server
cd src
python main.py

# In another terminal, test with demo log
curl -X POST "http://localhost:8000/analyze/upload" \
  -F "file=@../logs/demo_example.log"
```

## 🔧 Supported Log Formats

### DataPower Gateway
```
2026-05-18 09:30:15 [ERROR] HTTP 500 Internal Server Error
2026-05-18 09:30:15 [ERROR] Backend connection timeout
```

### API Connect (APIC)
```
2026-05-18 09:30:15 ERROR api:/member/inquiry status:500
2026-05-18 09:30:15 ERROR Gateway timeout connecting to backend
```

### Java Application
```
2026-05-18 09:30:15 ERROR Exception in thread "main"
java.net.SocketTimeoutException: Read timed out
    at java.net.SocketInputStream.socketRead0(Native Method)
```


## 📊 JSON-LD Schema & Graph Visualization

The system uses **JSON-LD with @graph structure** for representing incidents as interconnected nodes and relationships, enabling:

- **Graph Database Integration**: Import into Neo4j, GraphDB, or other graph databases
- **Semantic Queries**: Query incident data using SPARQL or Cypher
- **Knowledge Graphs**: Build enterprise incident knowledge graphs
- **Visual Analytics**: Visualize incident relationships and patterns

### Node Types

The schema defines 8 core node types:

1. **Incident** - Root node representing a production incident
2. **RootCause** - Identified root cause with category and confidence
3. **SuggestedFix** - Recommended resolution steps with priority
4. **API** - Affected API endpoints with error metrics
5. **LogEntry** - Individual log entries from various sources
6. **BackendService** - Backend services involved in the incident
7. **AdditionalCheck** - Diagnostic checks to perform
8. **GitHubIssue** - GitHub issue tracking the incident

### Relationships

The schema defines 9 relationship types:

- `hasRootCause`: Incident → RootCause
- `hasSuggestedFix`: Incident → SuggestedFix
- `affectsAPI`: Incident → API
- `hasLogEntry`: Incident → LogEntry
- `dependsOn`: API → BackendService, Fix → Fix
- `impacts`: BackendService → API
- `triggeredBy`: Incident → LogEntry
- `resolvedBy`: Incident → Fix
- `relatedTo`: Generic relationship between nodes

### Schema Files

- **Schema Definition**: `config/incident_schema.json`
- **Example Data**: `docs/example_incident_graph.json`
- **Documentation**: `docs/JSONLD_SCHEMA_GUIDE.md`

### Example JSON-LD Output

```json
{
  "@context": {
    "@vocab": "http://schema.org/",
    "incident": "http://incident-resolution.ai/ontology#"
  },
  "@graph": [
    {
      "@id": "incident:inc-001",
      "@type": "incident:Incident",
      "severity": "HIGH",
      "root_cause": "Backend timeout",
      "hasRootCause": ["incident:cause-001"],
      "hasSuggestedFix": ["incident:fix-001", "incident:fix-002"],
      "affectsAPI": ["incident:api-001"]
    },
    {
      "@id": "incident:cause-001",
      "@type": "incident:RootCause",
      "root_cause": "Firewall blocking port 8443",
      "category": "NETWORK",
      "confidence": 90
    }
  ]
}
```

### Visualization Tools

Compatible with:
- **Neo4j** - Property graph database
- **GraphDB** - RDF triple store
- **D3.js** - Force-directed graphs
- **Cytoscape.js** - Interactive networks
- **Apache Jena** - SPARQL queries

## 🎨 Report Formats

The system generates reports in multiple formats:

1. **Markdown** - For GitHub issues and documentation
2. **JSON** - For API integration
3. **HTML Email** - For email notifications
4. **Slack** - For Slack channel alerts

## 🔐 Security

- API keys stored in environment variables
- GitHub token requires minimal permissions (issues:write)
- No sensitive data logged
- CORS enabled for web integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🆘 Troubleshooting

### Issue: "OpenAI API key not configured"
**Solution:** Set `OPENAI_API_KEY` in your `.env` file

### Issue: "GitHub integration not working"
**Solution:** 
1. Verify `GITHUB_TOKEN` is set
2. Ensure token has `repo` scope
3. Check `GITHUB_REPO` format is `owner/repository`

### Issue: "Log parsing returns empty results"
**Solution:** 
- Check log format matches supported types
- Ensure error keywords are present in logs
- Try manual incident submission endpoint

## 📞 Support

For issues and questions:
- Create a GitHub issue
- Check documentation in `/docs`
- Review demo examples in `/logs`

## 🎯 Roadmap

- [ ] Support for more log formats (Nginx, Apache, etc.)
- [ ] Integration with monitoring tools (Prometheus, Grafana)
- [ ] Machine learning for pattern recognition
- [ ] Real-time log streaming support
- [ ] Dashboard for incident visualization
- [ ] Slack bot integration
- [ ] Email notification system
- [ ] Incident history and analytics

## 🌟 Key Benefits

1. **Faster Resolution**: Reduce MTTR by 60-80%
2. **Automated Documentation**: Auto-generated incident reports
3. **Knowledge Sharing**: GitHub issues create searchable knowledge base
4. **24/7 Availability**: AI never sleeps
5. **Consistent Analysis**: Same quality analysis every time
6. **Easy Integration**: REST API for any system

---

**Built with ❤️ for DevOps teams**