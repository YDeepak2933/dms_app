Dataset Management Service (FastAPI)
This project is a metadata-driven backend service built using FastAPI, SQLAlchemy ORM, and SQLite that allows you to manage:
1. Datasets (business entities like Customer, Order)
2. Data Elements (fields within datasets)
3. Relationships & constraints between datasets and elements
4. Search and filtering of data elements

# Next upgrades
1. Authentication (JWT)
2. Soft delete
3. Dataset versioning

#------------------ Running the Application ------------------#
1. Clone Project
git clone <repo-url>
cd project-folder

2. Create Virtual Environment
python -m venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

3. Install Dependencies
pip install requirements.txt

4. cd app-folder

5. Run the Application
uvicorn main:app --reload

6. Access API Docs (Swagger UI)
http://127.0.0.1:8000/docs

1. Run pytest
pytest -v


#--- Data Model & Design Decisions ---#
1. Core Entities

Dataset---
Represents a business entity such as:
Customer
Order

Fields:
id (UUID, Primary Key)
name (Unique)
description

DataElement---
Represents an attribute/field inside a dataset.

Examples:
email
date_of_birth

Fields:
id (UUID, Primary Key)
dataset_id (Foreign Key → Dataset)
name
data_type
is_required
is_unique

2. Relationships

One-to-Many Relationship
One Dataset → Many Data Elements

Implemented using SQLAlchemy relationship()

3. Key Constraints (Business Rules)
Unique Dataset Name
Each dataset must be unique:
name = Column(String, unique=True)

Unique Data Element per Dataset
A data element name cannot be duplicated within the same dataset:
UniqueConstraint("dataset_id", "name")
Example:
Allowed:Customer_email


Unique Data Element per Dataset
A data element name cannot be duplicated within the same dataset:
UniqueConstraint("dataset_id", "name")
Example:

Allowed:
Customer.email
Order.email

Not Allowed:
Customer.email (duplicate)

#---Referential Integrity---#
dataset_id is a foreign key
Ensures element always belongs to a valid dataset

Cascade Delete

Deleting a dataset also deletes its elements:
cascade="all, delete-orphan"

4. Design Decisions
UUID for IDs

Ensures global uniqueness
Avoids collisions

#---Metadata-driven approach---#
No hardcoded schema like Customer/Order
Everything is dynamic and configurable via API

#---SQLite as DB---#
Lightweight and easy setup
Good for development/testing

#---Separation of concerns---#
models.py → DB schema
schemas.py → API validation
crud.py → DB operations
main.py → API routes

FastAPI
Automatic Swagger documentation
Type validation using Pydantic

5. APIs Overview
Dataset APIs

POST /datasets → Create dataset
GET /datasets → List datasets
GET /datasets/{id} → Get dataset with elements

models.py → DB schema
schemas.py → API validation
crud.py → DB operations
main.py → API routes

#---Data Elements APIs---#

POST /datasets/{id}/elements → Add element
GET /datasets/{id}/elements → List elements

Search API

GET /elements/search
GET /datasets/{id}/elements/search

Supports filtering by:

name
data_type
is_required
is_unique