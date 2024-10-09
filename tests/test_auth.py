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
    response = client.post("/signup", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 201

def test_login(client):
    # Create user manually
    user = User(email="testuser@example.com")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()

    # Test login
    response = client.post("/login", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()
