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

def test_create_workout(client):
    # Create a user and login
    response = client.post("/signup", json={"email": "user@example.com", "password": "password"})
    assert response.status_code == 201
    login_response = client.post("/login", json={"email": "user@example.com", "password": "password"})
    token = login_response.get_json()["access_token"]

    # Create a new workout
    headers = {"Authorization": f"Bearer {token}"}
    workout_data = {
        "date": "2024-10-10",
        "comments": "Morning workout",
        "exercises": [
            {"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}
        ]
    }
    response = client.post("/workouts", json=workout_data, headers=headers)
    assert response.status_code == 201

def test_get_workouts(client):
    # Create a user and login
    response = client.post("/signup", json={"email": "user@example.com", "password": "password"})
    assert response.status_code == 201
    login_response = client.post("/login", json={"email": "user@example.com", "password": "password"})
    token = login_response.get_json()["access_token"]

    # Get the list of workouts (should be empty initially)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/workouts", headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 0
