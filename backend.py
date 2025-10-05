from fastapi import FastAPI, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Standard, Section
from parser import parse_standard_pdf
app = FastAPI()


from groq import Groq
import os


GROQ_API_KEY = "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"


groq_client = Groq(api_key=GROQ_API_KEY)

@app.get("/")
def root():
    return {"message": "Standards backend running 🚀"}

@app.get("/standards")
def list_standards(db: Session = Depends(get_db)):
    return db.query(Standard).all()

@app.get("/sections")
def list_sections(db: Session = Depends(get_db)):
    return db.query(Section).limit(100).all()

@app.post("/parse")
def parse_pdf(standard_name: str, version: str = None, file_path: str = None, start:int=0, db: Session = Depends(get_db)):
    """
    Example call:
    POST /parse?standard_name=ISO9001&file_path=files/ISO9001.pdf
    """
    parse_standard_pdf(file_path, db, standard_name, version,start)
    return {"message": f"Parsed {standard_name}"}


@app.get("/search")
def search_sections(q: str, standard_name: str, db: Session = Depends(get_db)):
    """
    Search for a keyword or phrase in section titles or content
    within a specific standard.

    Example:
        /search?q=risk&standard_name=ISO9001
    """
    if not q or len(q.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query string 'q' cannot be empty.")

    
    standard = db.query(Standard).filter(Standard.name == standard_name).first()
    if not standard:
        raise HTTPException(status_code=404, detail=f"Standard '{standard_name}' not found.")

    
    results = (
        db.query(Section)
        .filter(
            Section.standard_id == standard.id,
            (Section.title.ilike(f"%{q}%")) |
            (Section.content.ilike(f"%{q}%"))
        )
        .all()
    )

    if not results:
        return {"message": f"No matches found for '{q}' in standard '{standard_name}'."}

    return results

from pydantic import BaseModel
import re
class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat_with_groq(req: ChatRequest):
    try:
        response = groq_client.chat.completions.create(
            model="deepseek-r1-distill-llama-70B",   
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in project management. answer related questions clearly and concisely, othewise dont"},
                {"role": "user", "content": req.question + " Refuse to Answer if its not relevant to Project Management"},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        raw = response.choices[0].message.content
        cleaned = re.sub(r"^<think>.*?</think>\s*", "", raw, flags=re.DOTALL)
        return {"answer": cleaned.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
