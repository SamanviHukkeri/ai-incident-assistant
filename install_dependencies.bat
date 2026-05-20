@echo off
echo Installing AI Incident Assistant dependencies...
echo.
python -m pip install --upgrade pip
python -m pip install fastapi==0.109.0
python -m pip install uvicorn[standard]==0.27.0
python -m pip install pydantic==2.5.3
python -m pip install python-dotenv==1.0.0
python -m pip install openai==1.10.0
python -m pip install langchain==0.1.4
python -m pip install langchain-openai==0.0.5
python -m pip install PyGithub==2.1.1
python -m pip install python-dateutil==2.8.2
python -m pip install regex==2023.12.25
python -m pip install httpx==0.26.0
python -m pip install requests==2.31.0
python -m pip install pytest==7.4.4
python -m pip install pytest-asyncio==0.23.3
python -m pip install pytest-cov==4.1.0
python -m pip install pyyaml==6.0.1
python -m pip install jinja2==3.1.3
python -m pip install python-multipart
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure you have a .env file with your OPENAI_API_KEY
echo 2. Run: cd src
echo 3. Run: python main.py
echo.
pause

@REM Made with Bob
