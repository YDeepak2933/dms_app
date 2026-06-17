from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

#Test Case 1: API Endpoint Works (Create + Fetch Dataset)
def test_create_and_get_dataset():
    # Create dataset
    response = client.post("/datasets", json={
        "name": "TestDataset",
        "description": "Test Desc"
    })

    assert response.status_code == 200
    data = response.json()
    assert "id" in data

    dataset_id = data["id"]

    # Fetch dataset
    response = client.get(f"/datasets/{dataset_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "TestDataset"
    assert data["data_elements"] == []

# Test Case 2: Business Rule Enforcement
#UniqueConstraint("dataset_id", "name")

def test_unique_data_element_per_dataset():
    # Step 1: Create dataset
    response = client.post("/datasets", json={
        "name": "UniqueRuleTest1",
        "description": "Testing uniqueness"
    })
    assert response.status_code == 200
    dataset_id = response.json()["id"]

    # Step 2: Add first element
    response = client.post(f"/datasets/{dataset_id}/elements", json={
        "name": "email",
        "data_type": "string"
    })
    assert response.status_code == 200

    # Step 3: Add duplicate element (should FAIL)
    response = client.post(f"/datasets/{dataset_id}/elements", json={
        "name": "email",
        "data_type": "string"
    })

    # Expect failure due to constraint violation

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]
