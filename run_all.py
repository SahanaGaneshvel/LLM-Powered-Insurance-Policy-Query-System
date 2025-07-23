import subprocess
import sys
import os
import time

# Paths
BACKEND_CMD = [sys.executable, '-m', 'uvicorn', 'main:app', '--reload']
STREAMLIT_CMD = [sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py']

backend_proc = None
streamlit_proc = None

try:
    print('Starting FastAPI backend...')
    backend_proc = subprocess.Popen(BACKEND_CMD, cwd=os.path.dirname(__file__))
    time.sleep(3)  # Give backend time to start
    print('Starting Streamlit UI...')
    streamlit_proc = subprocess.Popen(STREAMLIT_CMD, cwd=os.path.dirname(__file__))
    print('Both backend and UI are running. Press Ctrl+C to stop.')
    backend_proc.wait()
except KeyboardInterrupt:
    print('\nShutting down...')
finally:
    if backend_proc:
        backend_proc.terminate()
    if streamlit_proc:
        streamlit_proc.terminate() 