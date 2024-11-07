import pytest
from src.tasks import app, worth, is_date_and_in_past, get_existing_or_create_db

@pytest.fixture
def test_app():
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(test_app):
    return test_app.test_client()

body = {
    "title": "test_task",
    "description": "this is a test task",
    "priority": 2,
    "difficulty": 2,
    "due_date": "2025-10-20"
}

# --- Step 1 ---

def test_add_task(teardown,client):
    with app.app_context():
        response = client.post('/tasks', json=body)
        assert response.status_code == 201
        task_data = response.get_json()
        assert task_data["title"] == body["title"]
        assert task_data["priority"] == body["priority"]
        assert task_data["difficulty"] == body["difficulty"]

def test_complete_task(client):
    with app.app_context():
        # Add a task
        response = client.post('/tasks', json=body)
        task_id = response.get_json()["id"]

        # Complete the task
        response = client.post(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Tâche marquée comme terminée"

def test_cleanup_tasks(client):
    with app.app_context():
        # Add a task with a past due date
        past_task = body.copy()
        past_task["due_date"] = "2022-01-01"
        client.post("/tasks", json=past_task)

        # Perform cleanup
        response = client.delete("/tasks/cleanup")
        assert response.status_code == 200
        assert "tâches obsolètes ou complétées supprimées" in response.get_json()["message"]

# --- Step 2 ---

def test_is_date_and_in_past():
    assert is_date_and_in_past("2020-01-01") == True
    assert is_date_and_in_past("2099-01-01") == False
    assert is_date_and_in_past(None) == False

def test_worth_calculation():
    assert worth(priority=2, difficulty=3, due_date="2020-01-01") == 30  # Past date, score halved
    assert worth(priority=2, difficulty=3, due_date="2099-01-01") == 60  # Future date, full score

# --- Step 3 ---

def test_complete_with_mock(mocker, client):
    with app.app_context():
        # Mock the 'worth' function to control score calculation
        mocker.patch("src.tasks.worth", return_value=100)

        # Add a task
        response = client.post('/tasks', json=body)
        task_id = response.get_json()["id"]

        # Complete the task and check if the mocked score is used
        response = client.post(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.get_json()["score_added"] == 100

# --- Step 4 ---

def test_task_lifecycle(client):
    with app.app_context():
        response = client.post("/tasks", json=body)
        task_id = response.get_json()["id"]

        response = client.get("/tasks/active")
        active_tasks = response.get_json()
        assert any(task["id"] == task_id for task in active_tasks), "Task should be active after creation."

        response = client.post(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Tâche marquée comme terminée"

        response = client.get("/tasks/active")
        active_tasks = response.get_json()
        assert not any(task["id"] == task_id for task in active_tasks), "Completed task should not appear in active tasks."

        response = client.delete("/tasks/cleanup")
        assert response.status_code == 200

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404, "Task should not exist after cleanup."

# --- Step 5 ---

def test_total_score(client):
    with app.app_context():
        response = client.post("/tasks", json=body)
        task_id1 = response.get_json()["id"]
        client.post(f"/tasks/{task_id1}/complete")

        another_task = body.copy()
        another_task["title"] = "another_test_task"
        response = client.post("/tasks", json=another_task)
        task_id2 = response.get_json()["id"]
        client.post(f"/tasks/{task_id2}/complete")

        response = client.get("/scores/total")
        assert response.status_code == 200
        assert response.get_json()["total_score"] > 0

# --- Step 6 ---

# pytest --cov=src.tasks --cov-report=html
