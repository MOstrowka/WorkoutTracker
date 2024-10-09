from flask import Blueprint, request, jsonify
from .models import User
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

# User registration
@auth_bp.route('/signup', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'description': 'Rejestracja nowego użytkownika',
    'parameters': [
        {
            'name': 'email',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Użytkownik został pomyślnie zarejestrowany'},
        409: {'description': 'Użytkownik już istnieje'}
    }
})
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# User login
@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'description': 'Logowanie użytkownika',
    'parameters': [
        {
            'name': 'login_data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Zalogowano pomyślnie, zwrócono token JWT'},
        401: {'description': 'Niepoprawne dane logowania'}
    }
})
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Protected route example (requires valid JWT token)
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Auth'],
    'description': 'Przykładowa chroniona trasa, wymaga ważnego tokenu JWT',
    'responses': {
        200: {'description': 'Zalogowany użytkownik został zwrócony'}
    }
})
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200
