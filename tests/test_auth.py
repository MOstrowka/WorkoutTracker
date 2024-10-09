import pytest
from app import create_app, db
from app.models import User

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

def test_signup(client):
    # Usuń użytkownika, jeśli istnieje
    user = User.query.filter_by(email="testuser@example.com").first()
    if user:
        db.session.delete(user)
        db.session.commit()

    # Test user signup
    response = client.post("/signup", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 201


def test_signup_existing_user(client):
    # Test user signup with existing user
    client.post("/signup", json={"email": "testuser@example.com", "password": "testpassword"})
    response = client.post("/signup", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 409  # User already exists
    assert response.get_json()["message"] == "User already exists"

def test_login(client):
    # Create user manually
    user = User(email="testuser@example.com")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()

    # Test login with correct credentials
    response = client.post("/login", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_invalid_user(client):
    # Test login with non-existing user
    response = client.post("/login", json={"email": "nonexistent@example.com", "password": "wrongpassword"})
    assert response.status_code == 401  # Invalid credentials
    assert response.get_json()["message"] == "Invalid credentials"

def test_login_invalid_password(client):
    # Create user manually
    user = User(email="testuser@example.com")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()

    # Test login with incorrect password
    response = client.post("/login", json={"email": "testuser@example.com", "password": "wrongpassword"})
    assert response.status_code == 401  # Invalid credentials
    assert response.get_json()["message"] == "Invalid credentials"
