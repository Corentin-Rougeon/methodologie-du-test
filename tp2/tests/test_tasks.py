import pytest
from src.tasks import app, worth, is_date_and_in_past, get_existing_or_create_db
from datetime import datetime


@pytest.fixture
def reset_db():
    with app.app_context():
        db = get_existing_or_create_db()
        cursor = db.cursor()
        # Clear tables to reset the state
        cursor.execute("DELETE FROM tasks")
        cursor.execute("DELETE FROM scores")
        db.commit()

@pytest.fixture
def teardown():
    yield
    # Close database after each test to prevent issues
    with app.app_context():
        db = get_existing_or_create_db()
        db.close()
@pytest.fixture
def test_app():
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(test_app):
    return test_app.test_client()

# Sample task data
body = {
    "title": "test_task",
    "description": "this is a test task",
    "priority": 2,
    "difficulty": 2,
    "due_date": "2025-10-20"
}

# --- Step 1: Functional and Black-Box Tests ---

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

# --- Step 2: White-Box Tests and Code Coverage ---

def test_is_date_and_in_past():
    assert is_date_and_in_past("2020-01-01") == True
    assert is_date_and_in_past("2099-01-01") == False
    assert is_date_and_in_past(None) == False

def test_worth_calculation():
    assert worth(priority=2, difficulty=3, due_date="2020-01-01") == 30  # Past date, score halved
    assert worth(priority=2, difficulty=3, due_date="2099-01-01") == 60  # Future date, full score

# --- Step 3: Mocking Dependencies ---

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

# --- Step 4: End-to-End (E2E) Tests ---

def test_task_lifecycle(client):
    with app.app_context():
        # Step 1: Add a new task
        response = client.post("/tasks", json=body)
        task_id = response.get_json()["id"]

        # Step 2: Verify that the task appears in active tasks
        response = client.get("/tasks/active")
        active_tasks = response.get_json()
        assert any(task["id"] == task_id for task in active_tasks), "Task should be active after creation."

        # Step 3: Complete the task
        response = client.post(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Tâche marquée comme terminée"

        # Step 4: Confirm the task no longer appears in active tasks
        response = client.get("/tasks/active")
        active_tasks = response.get_json()
        assert not any(task["id"] == task_id for task in active_tasks), "Completed task should not appear in active tasks."

        # Step 5: Clean up completed tasks
        response = client.delete("/tasks/cleanup")
        assert response.status_code == 200

        # Step 6: Verify the task is deleted
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404, "Task should not exist after cleanup."

# --- Step 5: Integration Tests and Database Validation ---

def test_total_score(client):
    with app.app_context():
        # Add and complete multiple tasks to check cumulative score
        response = client.post("/tasks", json=body)
        task_id1 = response.get_json()["id"]
        client.post(f"/tasks/{task_id1}/complete")

        another_task = body.copy()
        another_task["title"] = "another_test_task"
        response = client.post("/tasks", json=another_task)
        task_id2 = response.get_json()["id"]
        client.post(f"/tasks/{task_id2}/complete")

        # Fetch the total score and validate
        response = client.get("/scores/total")
        assert response.status_code == 200
        assert response.get_json()["total_score"] > 0  # Verify cumulative score is positive

# --- Step 6: Report Generation (optional in code, run with pytest-cov) ---

# To generate a coverage report in HTML:
# Run this command in the terminal:
# pytest --cov=src.tasks --cov-report=html
