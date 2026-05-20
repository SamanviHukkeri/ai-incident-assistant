# Installation Guide for Windows 🪟

## ⚠️ Python Not Found Error

If you see "Python was not found", you need to install Python first.

## 📥 Step 1: Install Python

### Option A: Download from Python.org (Recommended)

1. **Download Python 3.11 or higher:**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (latest version)

2. **Run the installer:**
   - ✅ **IMPORTANT:** Check "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify installation:**
   ```powershell
   python --version
   # Should show: Python 3.11.x
   ```

### Option B: Install from Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click "Get" or "Install"
4. Wait for installation

## 📦 Step 2: Install Project Dependencies

Once Python is installed:

```powershell
# Navigate to project directory
cd "c:\Personal\AI Dev\AIAgent\ai-incident-assistant"

# Install required packages
pip install -r requirements.txt
```

## 🔑 Step 3: Configure API Keys

1. **Copy environment template:**
   ```powershell
   copy .env.example .env
   ```

2. **Get OpenAI API Key:**
   - Go to: https://platform.openai.com/api-keys
   - Sign up or log in
   - Click "Create new secret key"
   - Copy the key (starts with `sk-test`)

3. **Edit .env file:**
   - Open `.env` in notepad or VS Code
   - Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

4. **Optional - GitHub Integration:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (for private repos) or `public_repo`
   - Copy token and add to `.env`:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_REPO=your-username/your-repo
   ```

## 🚀 Step 4: Run the Application

### Start the Server

```powershell
cd src
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test the Application

**Option 1: Use the Web Interface**
1. Keep the server running
2. Open `docs/demo.html` in your browser
3. Upload a log file or paste error message
4. Click "Analyze"

**Option 2: Use Command Line**

Open a NEW PowerShell window:
```powershell
cd "C:\Users\VijayakumarHukkeri\Downloads\ai-incident-assistant"

# Test with demo log file
curl -X POST "http://localhost:8000/analyze/upload" -F "file=@logs/demo_example.log"
```

**Option 3: Use Python Script**

```powershell
cd tests
python test_demo.py
```

## 🔧 Troubleshooting

### Issue: "pip is not recognized"

**Solution:**
```powershell
python -m pip install -r requirements.txt
```

### Issue: "Module not found" errors

**Solution:**
```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Port 8000 already in use

**Solution:**
Edit `src/main.py` and change the port:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001)
```

### Issue: OpenAI API errors

**Check:**
1. API key is correct in `.env`
2. You have credits in your OpenAI account
3. No spaces or quotes around the key

### Issue: Can't find curl command

**Solution:** Use PowerShell's Invoke-WebRequest:
```powershell
$file = Get-Item "logs\demo_example.log"
$form = @{
    file = $file
}
Invoke-WebRequest -Uri "http://localhost:8000/analyze/upload" -Method Post -Form $form
```

Or just use the web interface (`docs/demo.html`)!

## 📝 Quick Reference

### Start Server
```powershell
cd "C:\Users\VijayakumarHukkeri\Downloads\ai-incident-assistant\src"
python main.py
```

### Run Tests
```powershell
cd "C:\Users\VijayakumarHukkeri\Downloads\ai-incident-assistant\tests"
python test_demo.py
```

### View API Documentation
Open browser: http://localhost:8000/docs

### Use Web Interface
Open in browser: `file:///C:/Users/VijayakumarHukkeri/Downloads/ai-incident-assistant/ai-incident-assistant/docs/docs/demo.html`

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] `python --version` works
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with OpenAI API key
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/health
- [ ] Demo test runs successfully

## 🎯 Next Steps After Installation

1. **Test with demo log:**
   ```powershell
   cd tests
   python test_demo.py
   ```

2. **Try the web interface:**
   - Open `docs/demo.html`
   - Upload `logs/demo_example.log`
   - See the AI analysis in action!

3. **Upload your own logs:**
   - Use the web interface or API
   - Get instant root cause analysis

4. **Configure GitHub integration:**
   - Add GitHub token to `.env`
   - Issues will be created automatically

## 📞 Need Help?

1. Check the main README.md
2. Review QUICKSTART.md
3. Check PROJECT_SUMMARY.md for overview
4. All documentation is in the `docs/` folder

---

**Once Python is installed, the setup takes less than 5 minutes!** 🚀