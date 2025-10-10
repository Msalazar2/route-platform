from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter()

@router.get("/notes", response_model=list[schemas.NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).order_by(models.Note.id.desc()).limit(100).all()

@router.post("/notes", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.NoteCreate, db: Session = Depends(get_db)):
    note = models.Note(body=payload.body, author=payload.author)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
