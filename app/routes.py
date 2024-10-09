from flask import Blueprint, request, jsonify
from .models import Workout, Exercise, db
from flask_jwt_extended import jwt_required, get_jwt_identity

workouts_bp = Blueprint('workouts', __name__)

# Create a new workout with exercises
@workouts_bp.route('/workouts', methods=['POST'])
@jwt_required()
def create_workout():
    user_id = get_jwt_identity()
    data = request.json
    workout_date = data.get('date')
    comments = data.get('comments')
    exercises = data.get('exercises')

    new_workout = Workout(user_id=user_id, date=workout_date, comments=comments)
    db.session.add(new_workout)
    db.session.commit()

    for exercise in exercises:
        new_exercise = Exercise(
            workout_id=new_workout.id,
            name=exercise['name'],
            description=exercise.get('description'),
            category=exercise['category'],
            repetitions=exercise['repetitions'],
            sets=exercise['sets'],
            weight=exercise['weight']
        )
        db.session.add(new_exercise)

    db.session.commit()
    return jsonify({"message": "Workout created successfully"}), 201

# Get all workouts for the current user
@workouts_bp.route('/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()
    workouts = Workout.query.filter_by(user_id=user_id).all()

    response = []
    for workout in workouts:
        exercises = Exercise.query.filter_by(workout_id=workout.id).all()
        exercise_list = [{
            "name": e.name,
            "description": e.description,
            "category": e.category,
            "repetitions": e.repetitions,
            "sets": e.sets,
            "weight": e.weight
        } for e in exercises]

        response.append({
            "id": workout.id,
            "date": workout.date,
            "comments": workout.comments,
            "exercises": exercise_list
        })

    return jsonify(response), 200

# Update an existing workout
@workouts_bp.route('/workouts/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"message": "Workout not found"}), 404

    data = request.json
    workout.date = data.get('date', workout.date)
    workout.comments = data.get('comments', workout.comments)
    db.session.commit()

    return jsonify({"message": "Workout updated successfully"}), 200

# Delete a workout
@workouts_bp.route('/workouts/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"message": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted successfully"}), 200

# Add a new exercise to an existing workout
@workouts_bp.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
@jwt_required()
def add_exercise_to_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"message": "Workout not found"}), 404

    data = request.json
    new_exercise = Exercise(
        workout_id=workout.id,
        name=data.get('name'),
        description=data.get('description'),
        category=data.get('category'),
        repetitions=data.get('repetitions'),
        sets=data.get('sets'),
        weight=data.get('weight')
    )

    db.session.add(new_exercise)
    db.session.commit()

    return jsonify({"message": "Exercise added successfully"}), 201

# Get all exercises for a specific workout
@workouts_bp.route('/workouts/<int:workout_id>/exercises', methods=['GET'])
@jwt_required()
def get_exercises_for_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({"message": "Workout not found"}), 404

    exercises = Exercise.query.filter_by(workout_id=workout_id).all()
    exercise_list = [{
        "name": e.name,
        "description": e.description,
        "category": e.category,
        "repetitions": e.repetitions,
        "sets": e.sets,
        "weight": e.weight
    } for e in exercises]

    return jsonify(exercise_list), 200
