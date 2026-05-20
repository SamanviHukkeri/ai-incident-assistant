# Quick Start Guide 🚀

Get the AI Incident Resolution Assistant running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- OpenAI API key (get one at https://platform.openai.com)
- GitHub Personal Access Token (optional, for issue creation)

## Step 1: Install Dependencies

```bash
cd ai-incident-assistant
pip install -r requirements.txt
```

## Step 2: Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
GITHUB_TOKEN=ghp_your_github_token_here  # Optional
GITHUB_REPO=owner/repository              # Optional
```

## Step 3: Run the Application

```bash
cd src
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 4: Test with Demo Example

Open a new terminal and run:

```bash
# Test the demo log file
curl -X POST "http://localhost:8000/analyze/upload" \
  -F "file=@logs/demo_example.log" \
  -F "create_github_issue=false"
```

Or run the test script:

```bash
cd tests
python test_demo.py
```

## Step 5: Try Manual Analysis

```bash
curl -X POST "http://localhost:8000/analyze/manual" \
  -H "Content-Type: application/json" \
  -d '{
    "error_message": "HTTP 500 - Backend timeout after 30 seconds",
    "log_type": "DATAPOWER",
    "create_github_issue": false
  }'
```

## Expected Output

```json
{
  "root_cause": "Backend connection timeout - possible firewall or network issue",
  "suggested_fixes": [
    "Check firewall rules between gateway and backend",
    "Verify backend service health and connectivity",
    "Review backend latency metrics",
    "Increase timeout configuration if needed"
  ],
  "affected_apis": [
    "/member/inquiry",
    "/claim/details"
  ],
  "severity": "HIGH",
  "github_issue_url": null,
  "incident_summary": "# Incident Report\n..."
}
```

## Web Interface (Optional)

Open your browser and visit:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "OpenAI API key not configured"
Make sure your `.env` file has:
```env
OPENAI_API_KEY=sk-your-actual-key
```

### Port 8000 already in use
Change the port in `src/main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001)
```

## Next Steps

1. ✅ Upload your own log files
2. ✅ Configure GitHub integration for automatic issue creation
3. ✅ Integrate with your monitoring system
4. ✅ Set up Slack notifications
5. ✅ Customize log parsing patterns

## Need Help?

- Check the main [README.md](../README.md)
- Review [API Documentation](http://localhost:8000/docs)
- Run the demo: `python tests/test_demo.py`

---

**You're all set! 🎉**