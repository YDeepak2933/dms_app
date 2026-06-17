from sqlalchemy.orm import Session
from app import models, schemas

# -------- Dataset --------

def create_dataset(db: Session, dataset: schemas.DatasetCreate):
    db_dataset = models.Dataset(
        name=dataset.name,
        description=dataset.description
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def get_datasets(db: Session):
    return db.query(models.Dataset).all()

def get_dataset(db: Session, dataset_id: str):
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()

# -------- Data Element --------

def create_data_element(db: Session, dataset_id: str, element: schemas.DataElementCreate):
    db_element = models.DataElement(
        dataset_id=dataset_id,
        name=element.name,
        data_type=element.data_type,
        is_required=element.is_required,
        is_unique=element.is_unique
    )
    db.add(db_element)
    db.commit()
    db.refresh(db_element)
    return db_element

def get_elements(db: Session, dataset_id: str):
    return db.query(models.DataElement).filter(
        models.DataElement.dataset_id == dataset_id
    ).all()

def search_data_elements(
    db,
    dataset_id: str = None,
    name: str = None,
    data_type: str = None,
    is_required: bool = None,
    is_unique: bool = None,
):
    query = db.query(models.DataElement)

    if dataset_id:
        query = query.filter(models.DataElement.dataset_id == dataset_id)

    if name:
        query = query.filter(models.DataElement.name.ilike(f"%{name}%"))

    if data_type:
        query = query.filter(models.DataElement.data_type == data_type)

    if is_required is not None:
        query = query.filter(models.DataElement.is_required == is_required)

    if is_unique is not None:
        query = query.filter(models.DataElement.is_unique == is_unique)

    return query.all()

