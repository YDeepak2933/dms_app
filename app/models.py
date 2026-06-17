import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Relationship
    data_elements = relationship(
        "DataElement",
        back_populates="dataset",
        cascade="all, delete-orphan"
    )

class DataElement(Base):
    __tablename__ = "data_elements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)

    name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)

    is_required = Column(Boolean, default=False)
    is_unique = Column(Boolean, default=False)

    # Relationship
    dataset = relationship("Dataset", back_populates="data_elements")

    # Constraint: unique element per dataset
    __table_args__ = (
        UniqueConstraint("dataset_id", "name", name="uq_dataset_element"),
    )
