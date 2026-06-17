from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas, crud
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dataset Management API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- Dataset APIs --------

@app.post("/datasets", response_model=schemas.DatasetResponse)
def create_dataset(dataset: schemas.DatasetCreate, db: Session = Depends(get_db)):
    return crud.create_dataset(db, dataset)


@app.get("/datasets", response_model=list[schemas.DatasetResponse])
def get_datasets(db: Session = Depends(get_db)):
    return crud.get_datasets(db)

@app.get("/datasets/{dataset_id}", response_model=schemas.DatasetWithElements)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = crud.get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

# -------- Data Element APIs --------

@app.post("/datasets/{dataset_id}/elements", response_model=schemas.DataElementResponse)
def create_element(dataset_id: str, element: schemas.DataElementCreate, db: Session = Depends(get_db)):
    dataset = crud.get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    try:
        return crud.create_data_element(db, dataset_id, element)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Data element already exists in this dataset"
        )

@app.get("/datasets/{dataset_id}/elements", response_model=list[schemas.DataElementResponse])
def get_elements(dataset_id: str, db: Session = Depends(get_db)):
    return crud.get_elements(db, dataset_id)

#------------ Data Elements Searching ----------------
@app.get("/elements/search", response_model=list[schemas.DataElementResponse])
def search_elements(
    name: str = None,
    data_type: str = None,
    is_required: bool = None,
    is_unique: bool = None,
    db: Session = Depends(get_db)
):
    results = crud.search_data_elements(
        db,
        name=name,
        data_type=data_type,
        is_required=is_required,
        is_unique=is_unique
    )
    return results

