# Assignment -1 
Repository for Agentic Assignment 2

# Windows - UV Prompt
#   Commands                What it does
    uv sync                 Install or update all packages
    uv add package-name     Add a new package
    uv run app.py           Run the main program
    python app.py           Run the main program
    uv run pytest           Run tests
    uv run ruff format .    Format your code nicely



# 🚀 Quick Start
### Step 1: Download the Project

1. Go to this GitHub repository
2. Click on **Code** → **Download ZIP**  OR  copy the repository URL
3. Extract the ZIP file to a folder on your computer
4. Open **Cursor** (or VS Code)

### Step 2: Open the Project in Cursor

- In Cursor, go to **File → Open Folder**
- Select the folder where you extracted the project (eg C:\`agentic-day1`)
## Prerequisites
- Python 3.12+
- Git
- UV
   ### 1. Install uv
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

   ### 2. Fix powershell Execution policy windows
   powershell Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
 

### Step 3:Setting Up API Keys
After running the copy command:
cp .env.example .env

Open the .env file
Replace the placeholders with your actual keys:

env# ==================== LLM API KEYS ====================

OPENAI_API_KEY=sk-your-actual-openai-key-here
GOOGLE_API_KEY=your-actual-google-gemini-key-here

Where to get API keys:

OpenAI: https://platform.openai.com/api-keys
Google Gemini: https://aistudio.google.com/app/apikey

### Step 4: Clone the repository
git clone https://github.com/reeverodrigues-oss/week1-assignment2.git


### Step 5. Create virtual environment
uv venv

### Step 6. Install dependencies
uv pip install -r requirements.txt

### Step 7. Activate the venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

### Step 7. Run the application
python app.py

