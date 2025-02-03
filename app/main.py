from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load student marks from q-vercel-python.json using absolute path
current_dir = os.path.dirname(os.path.realpath(__file__))
json_path = os.path.join(current_dir, "q-vercel-python.json")

try:
    with open(json_path) as f:
        students_data = json.load(f)
        student_marks = {student["name"]: student["marks"] for student in students_data}
except Exception as e:
    print(f"Error loading JSON file: {e}")
    student_marks = {}

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/api")
async def get_marks(name: list[str] = Query(...)):
    marks = []
    for student in name:
        if student in student_marks:
            marks.append(student_marks[student])
        else:
            raise HTTPException(status_code=404, detail=f"Student {student} not found")
    return {"marks": marks}

@app.get("/test")
async def test():
    """Test endpoint to verify data loading"""
    return {
        "total_students": len(student_marks),
        "sample_students": list(student_marks.keys())[:5],
        "status": "working"
    }
