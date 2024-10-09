from . import db
from .models import Exercise

def seed_exercises():
    exercises = [
        # Bodyweight Exercises (without weights)
        {"name": "Push-up", "description": "Bodyweight exercise for chest and triceps", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0},
        {"name": "Squat", "description": "Bodyweight squat for legs and glutes", "category": "Bodyweight", "repetitions": 20, "sets": 3, "weight": 0},
        {"name": "Plank", "description": "Core exercise for abs and back stability", "category": "Core", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Lunges", "description": "Bodyweight lunges for legs and balance", "category": "Bodyweight", "repetitions": 12, "sets": 3, "weight": 0},
        {"name": "Burpees", "description": "Full body cardio exercise", "category": "Bodyweight", "repetitions": 10, "sets": 3, "weight": 0},
        {"name": "Mountain Climbers", "description": "Cardio exercise for core and endurance", "category": "Bodyweight", "repetitions": 20, "sets": 3, "weight": 0},
        {"name": "Pull-up", "description": "Upper body exercise targeting back and biceps", "category": "Bodyweight", "repetitions": 10, "sets": 3, "weight": 0},
        {"name": "Dips", "description": "Triceps exercise using bodyweight", "category": "Bodyweight", "repetitions": 12, "sets": 3, "weight": 0},

        # Free Weight Exercises (using dumbbells/barbells)
        {"name": "Bench Press", "description": "Chest exercise using a barbell", "category": "Free Weights", "repetitions": 10, "sets": 3, "weight": 50},
        {"name": "Bicep Curl", "description": "Bicep exercise using dumbbells", "category": "Free Weights", "repetitions": 12, "sets": 3, "weight": 15},
        {"name": "Deadlift", "description": "Strength exercise for back and hamstrings using a barbell", "category": "Free Weights", "repetitions": 10, "sets": 3, "weight": 60},
        {"name": "Overhead Press", "description": "Shoulder exercise using dumbbells or barbell", "category": "Free Weights", "repetitions": 8, "sets": 3, "weight": 30},
        {"name": "Bent Over Row", "description": "Back exercise using a barbell", "category": "Free Weights", "repetitions": 10, "sets": 3, "weight": 40},
        {"name": "Dumbbell Fly", "description": "Chest exercise using dumbbells", "category": "Free Weights", "repetitions": 12, "sets": 3, "weight": 20},
        {"name": "Dumbbell Lateral Raise", "description": "Shoulder exercise using dumbbells", "category": "Free Weights", "repetitions": 12, "sets": 3, "weight": 10},
        {"name": "Front Squat", "description": "Leg exercise using a barbell", "category": "Free Weights", "repetitions": 8, "sets": 3, "weight": 50},

        # Machine Exercises (using gym machines)
        {"name": "Leg Press", "description": "Leg exercise using the leg press machine", "category": "Machine", "repetitions": 12, "sets": 3, "weight": 100},
        {"name": "Cable Row", "description": "Back exercise using a cable row machine", "category": "Machine", "repetitions": 12, "sets": 3, "weight": 50},
        {"name": "Lat Pulldown", "description": "Back exercise using the lat pulldown machine", "category": "Machine", "repetitions": 10, "sets": 3, "weight": 60},
        {"name": "Leg Curl", "description": "Hamstring exercise using the leg curl machine", "category": "Machine", "repetitions": 15, "sets": 3, "weight": 40},
        {"name": "Chest Press", "description": "Chest exercise using the chest press machine", "category": "Machine", "repetitions": 10, "sets": 3, "weight": 70},
        {"name": "Leg Extension", "description": "Quad exercise using the leg extension machine", "category": "Machine", "repetitions": 12, "sets": 3, "weight": 50},
        {"name": "Seated Row Machine", "description": "Back exercise using a seated row machine", "category": "Machine", "repetitions": 10, "sets": 3, "weight": 55},
        {"name": "Pec Deck Machine", "description": "Chest exercise using the pec deck machine", "category": "Machine", "repetitions": 12, "sets": 3, "weight": 40},

        # Cardio Exercises (running, biking, etc.)
        {"name": "Running", "description": "Cardio exercise for endurance", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},
        {"name": "Cycling", "description": "Cardio exercise using a stationary bike", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},
        {"name": "Treadmill Running", "description": "Running on the treadmill", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},
        {"name": "Rowing", "description": "Full body cardio exercise using a rowing machine", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},
        {"name": "Elliptical", "description": "Low impact cardio exercise using an elliptical machine", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},
        {"name": "Jump Rope", "description": "Cardio exercise for agility and endurance", "category": "Cardio", "repetitions": 100, "sets": 3, "weight": 0},
        {"name": "Swimming", "description": "Full body cardio exercise", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},
        {"name": "Stair Climber", "description": "Cardio exercise for lower body endurance", "category": "Cardio", "repetitions": 1, "sets": 1, "weight": 0},

        # Stretching/Flexibility Exercises
        {"name": "Hamstring Stretch", "description": "Stretching exercise for the hamstrings", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Quadriceps Stretch", "description": "Stretching exercise for the quadriceps", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Shoulder Stretch", "description": "Stretching exercise for the shoulders", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Triceps Stretch", "description": "Stretching exercise for the triceps", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Hip Flexor Stretch", "description": "Stretching exercise for the hip flexors", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Chest Stretch", "description": "Stretching exercise for the chest muscles", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Cat-Cow Stretch", "description": "Back and core flexibility exercise", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0},
        {"name": "Child's Pose", "description": "Relaxing stretch for the lower back", "category": "Flexibility", "repetitions": 1, "sets": 3, "weight": 0}
    ]

    for exercise_data in exercises:
        exercise = Exercise(
            name=exercise_data['name'],
            description=exercise_data['description'],
            category=exercise_data['category'],
            repetitions=exercise_data['repetitions'],
            sets=exercise_data['sets'],
            weight=exercise_data['weight']
        )
        db.session.add(exercise)

    db.session.commit()
    print("Exercises seeded successfully.")
