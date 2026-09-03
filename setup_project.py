"""
Smart Fertilizer Recommendation System — One-Click Automated Setup Script
Run this script on a new laptop/machine to set up the entire project:

Usage:
    python setup_project.py

What this script does:
1. Checks system prerequisites (Python 3.10+, Node.js, npm).
2. Creates `.env` configuration file for the backend if missing.
3. Installs backend Python dependencies (`pip install -r backend/requirements.txt`).
4. Trains the RandomForest ML model and generates `fertilizer_model.pkl`.
5. Installs frontend Node.js packages (`npm install` inside `frontend`).
6. Optionally starts both backend and frontend servers!
"""

import os
import sys
import subprocess
import shutil
import platform

# Color helpers for terminal output
def print_step(msg):
    print(f"\n\033[1;36m===> {msg}\033[0m" if sys.stdout.isatty() else f"\n===> {msg}")

def print_success(msg):
    print(f"\033[1;32m[✓] {msg}\033[0m" if sys.stdout.isatty() else f"[✓] {msg}")

def print_warning(msg):
    print(f"\033[1;33m[!] {msg}\033[0m" if sys.stdout.isatty() else f"[!] {msg}")

def print_error(msg):
    print(f"\033[1;31m[✗] {msg}\033[0m" if sys.stdout.isatty() else f"[✗] {msg}")


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")


def check_prerequisites():
    print_step("Step 1: Checking System Prerequisites")

    # Python version check
    py_ver = sys.version_info
    print(f"  • Python Version: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    if py_ver.major < 3 or (py_ver.major == 3 and py_ver.minor < 9):
        print_error("Python 3.9 or higher is required. Please upgrade Python.")
        sys.exit(1)

    # Node.js check
    node_path = shutil.which("node")
    if not node_path:
        print_error("Node.js is not installed or not in PATH! Please install Node.js (https://nodejs.org/).")
        sys.exit(1)
    else:
        try:
            node_ver = subprocess.check_output(["node", "-v"], text=True).strip()
            print(f"  • Node.js Version: {node_ver}")
        except Exception:
            pass

    # npm check
    npm_path = shutil.which("npm")
    if not npm_path:
        print_error("npm is not installed or not in PATH!")
        sys.exit(1)
    else:
        try:
            npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            print(f"  • npm Version: {npm_ver}")
        except Exception:
            pass

    print_success("All prerequisites satisfied.")


def setup_backend_env():
    print_step("Step 2: Configuring Backend Environment File (.env)")
    env_file = os.path.join(BACKEND_DIR, ".env")
    env_example = os.path.join(BACKEND_DIR, ".env.example")

    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            shutil.copy(env_example, env_file)
            print_success("Created backend/.env from .env.example")
        else:
            with open(env_file, "w") as f:
                f.write(
                    "SECRET_KEY=supersecretkey-change-in-production\n"
                    "ALGORITHM=HS256\n"
                    "ACCESS_TOKEN_EXPIRE_MINUTES=60\n"
                    "GEMINI_API_KEY=\n"
                    "DATABASE_URL=sqlite:///./fertilizer.db\n"
                )
            print_success("Created default backend/.env")
    else:
        print_success("backend/.env already exists.")


def install_backend_deps():
    print_step("Step 3: Installing Python Dependencies")
    req_file = os.path.join(BACKEND_DIR, "requirements.txt")
    if not os.path.exists(req_file):
        print_error(f"requirements.txt not found at {req_file}")
        sys.exit(1)

    cmd = [sys.executable, "-m", "pip", "install", "-r", req_file]
    print(f"  Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BACKEND_DIR)
    if result.returncode != 0:
        print_error("Failed to install Python dependencies.")
        sys.exit(1)
    print_success("Python dependencies installed successfully.")


def train_ml_model():
    print_step("Step 4: Training RandomForest Classifier Model")
    train_script = os.path.join(BACKEND_DIR, "ml", "train_model.py")
    if not os.path.exists(train_script):
        print_warning("ml/train_model.py not found. Skipping offline model training.")
        return

    cmd = [sys.executable, train_script]
    print(f"  Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BACKEND_DIR)
    if result.returncode != 0:
        print_warning("Model training exited with an error. Server will train on startup if needed.")
    else:
        print_success("RandomForest model trained and saved as ml/fertilizer_model.pkl.")


def install_frontend_deps():
    print_step("Step 5: Installing Frontend Node.js Dependencies")
    pkg_file = os.path.join(FRONTEND_DIR, "package.json")
    if not os.path.exists(pkg_file):
        print_error(f"package.json not found at {pkg_file}")
        sys.exit(1)

    # Use npx / npm depending on platform
    cmd = "npm.cmd" if platform.system() == "Windows" else "npm"
    print(f"  Executing: {cmd} install inside {FRONTEND_DIR}")
    result = subprocess.run([cmd, "install"], cwd=FRONTEND_DIR, shell=(platform.system() == "Windows"))
    if result.returncode != 0:
        print_error("Failed to install frontend dependencies.")
        sys.exit(1)
    print_success("Frontend Node.js packages installed successfully.")


def launch_prompt():
    print_step("Setup Complete! 🚀")
    print("""
\033[1;32m===================================================================
All dependencies installed & project setup successfully!
===================================================================\033[0m

To run the application manually on your new machine:

\033[1;33mTerminal 1 — Backend (FastAPI):\033[0m
  cd backend
  python run.py
  (Runs on http://localhost:8000)

\033[1;33mTerminal 2 — Frontend (React/Vite):\033[0m
  cd frontend
  npm run dev
  (Runs on http://localhost:5173)
""")

    answer = input("Would you like to start both backend & frontend servers now? (y/N): ").strip().lower()
    if answer in ("y", "yes"):
        print_step("Launching Backend and Frontend...")
        
        # Start backend
        backend_proc = subprocess.Popen(
            [sys.executable, "run.py"],
            cwd=BACKEND_DIR
        )
        print_success("Backend server started on http://localhost:8000")

        # Start frontend
        cmd_npm = "npm.cmd" if platform.system() == "Windows" else "npm"
        frontend_proc = subprocess.Popen(
            [cmd_npm, "run", "dev"],
            cwd=FRONTEND_DIR,
            shell=(platform.system() == "Windows")
        )
        print_success("Frontend dev server started on http://localhost:5173")

        try:
            backend_proc.wait()
            frontend_proc.wait()
        except KeyboardInterrupt:
            print("\nShutting down servers...")
            backend_proc.terminate()
            frontend_proc.terminate()


if __name__ == "__main__":
    print("\n=========================================================")
    print(" Smart Fertilizer Recommendation System — Project Installer")
    print("=========================================================")
    
    check_prerequisites()
    setup_backend_env()
    install_backend_deps()
    train_ml_model()
    install_frontend_deps()
    launch_prompt()
