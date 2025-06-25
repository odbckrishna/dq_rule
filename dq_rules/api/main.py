from fastapi import FastAPI, Query
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class RunRequest(BaseModel):
    dataset: str
    output: str

@app.post("/run-dq")
def run_dq(request: RunRequest):
    # Call the main rule engine script
    result = subprocess.run([
        'python', os.path.join(os.path.dirname(__file__), '..', 'main.py'),
        '--dataset', request.dataset,
        '--output', request.output
    ], capture_output=True, text=True)
    if result.returncode == 0:
        return {"status": "success", "output": request.output}
    else:
        return {"status": "error", "details": result.stderr}
