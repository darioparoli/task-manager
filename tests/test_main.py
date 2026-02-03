"""
Unit tests for Task Manager API
"""
from tabnanny import check
import pytest
from fastapi.testclient import TestClient
from main import app, tasks_db, task_id_counter


@pytest.fixture
def client():
    """Create a test client"""
    # Reset the tasks database and counter before each test
    global task_id_counter
    tasks_db.clear()
    task_id_counter = 1
    return TestClient(app)


def test_create_task(client):
    """Test creating a new task"""
    # Create a new task
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    
    # Verify the response
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_get_tasks(client):
    """Test getting all tasks"""
    # Create some tasks
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})
    
    # Get all tasks
    response = client.get("/api/tasks")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_single_task(client):
    """Test getting a single task by ID"""
    # Create a task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Single Task", "description": "Description"}
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/api/tasks/{task_id}")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Task"
    assert data["description"] == "Description"


def test_get_nonexistent_task(client):
    """Test getting a task that doesn't exist"""
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


def test_update_task(client):
    """Test updating a task"""
    # Create a task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original Task"}
    )
    task_id = create_response.json()["id"]
    created_at = create_response.json()["created_at"]
    
    # Update the task
    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "id": task_id,
            "title": "Updated Task",
            "description": "New Description",
            "completed": True,
            "created_at": created_at
        }
    )
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "New Description"
    assert data["completed"] is True


def test_delete_task(client):
    """Test deleting a task"""
    # Create a task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Task to Delete"}
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}")
    
    # Verify the response
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    
    # Verify the task is gone
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task(client):
    """Test deleting a task that doesn't exist"""
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404

def test_delete_completed_tasks(client):
    """Test deleting all completed tasks"""
    # 1. Crea un task e prendi l'ID che decide il SERVER
    post_res = client.post("/api/tasks", json={"title": "Test", "description": "Check"})
    task = post_res.json()
    task_id = task["id"]

    # 2. Modifica lo stato a completed: True
    task["completed"] = True
    put_res = client.put(f"/api/tasks/{task_id}", json=task)
    
    # DEBUG: Se questo fallisce, il problema è nella PUT
    assert put_res.status_code == 200 
    assert put_res.json()["completed"] is True

    # 3. Ora la DELETE dovrebbe trovare 1 task completato
    del_res = client.delete("/api/tasks/completed")
    assert del_res.json()["message"] == "Eliminati 1 task"

