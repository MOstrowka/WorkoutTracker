import pytest
from app import create_app, db
from app.models import User, Workout

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    # Create a user and get an authorization token
    client.post("/signup", json={"email": "user@example.com", "password": "password"})
    login_response = client.post("/login", json={"email": "user@example.com", "password": "password"})
    return login_response.get_json()["access_token"]

def test_create_workout(client, auth_token):
    # Create a new workout
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_data = {
        "date": "2024-10-10",
        "comments": "Morning workout",
        "exercises": [
            {"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}
        ]
    }
    response = client.post("/workouts", json=workout_data, headers=headers)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Workout created successfully"

def test_get_workouts(client, auth_token):
    # Create a workout first
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_data = {
        "date": "2024-10-10",
        "comments": "Morning workout",
        "exercises": [
            {"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}
        ]
    }
    client.post("/workouts", json=workout_data, headers=headers)

    # Get the list of workouts
    response = client.get("/workouts", headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_update_workout(client, auth_token):
    # Create a workout first
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_data = {
        "date": "2024-10-10",
        "comments": "Morning workout",
        "exercises": [
            {"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}
        ]
    }
    client.post("/workouts", json=workout_data, headers=headers)

    # Update the workout
    update_data = {
        "date": "2024-10-12",
        "comments": "Updated workout"
    }
    response = client.put("/workouts/1", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Workout updated successfully"

def test_delete_workout(client, auth_token):
    # Create a workout first
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_data = {
        "date": "2024-10-10",
        "comments": "Morning workout",
        "exercises": [
            {"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}
        ]
    }
    client.post("/workouts", json=workout_data, headers=headers)

    # Delete the workout
    response = client.delete("/workouts/1", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Workout deleted successfully"

def test_generate_report(client, auth_token):
    # Create a workout first
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_data = {
        "date": "2023-10-10",  # past date for report generation
        "comments": "Morning workout",
        "exercises": [
            {"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}
        ]
    }
    client.post("/workouts", json=workout_data, headers=headers)

    # Generate report
    response = client.get("/workouts/report", headers=headers)
    assert response.status_code == 200
    report = response.get_json()
    assert report["total_workouts"] == 1
    assert len(report["workouts"]) == 1
    assert report["workouts"][0]["comments"] == "Morning workout"
