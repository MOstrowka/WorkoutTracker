
# Workout Tracker API

This is a Flask-based API for a workout tracker application where users can sign up, log in, create workout plans, and track their progress. The API supports JWT-based authentication and CRUD operations on workouts.

## Features
- **User Authentication:** Users can sign up, log in, and get access tokens using JSON Web Tokens (JWT).
- **Workout Management:** Users can create, update, and delete workout plans. Each workout can contain multiple exercises.
- **Reports:** Users can generate reports of their past workouts.
- **Secure Endpoints:** All workout-related operations require authentication via JWT.

## Technologies
- **Flask** for API framework
- **Flask-SQLAlchemy** for database ORM
- **Flask-JWT-Extended** for JWT authentication
- **Flask-Migrate** for database migrations
- **SQLite** as the database
- **Pytest** for testing

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/workout-tracker.git
    cd workout-tracker
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Usage

1. Run the Flask development server:
    ```bash
    flask run
    ```

2. The API will be available at `http://127.0.0.1:5000`.

## Endpoints

### User Authentication
- **Sign Up**
    - Endpoint: `/signup`
    - Method: `POST`
    - Request body: 
      ```json
      {
        "email": "user@example.com",
        "password": "password"
      }
      ```

- **Log In**
    - Endpoint: `/login`
    - Method: `POST`
    - Request body: 
      ```json
      {
        "email": "user@example.com",
        "password": "password"
      }
      ```
    - Response: Access token (JWT)

### Workout Management
- **Create Workout**
    - Endpoint: `/workouts`
    - Method: `POST`
    - Request body:
      ```json
      {
        "date": "YYYY-MM-DD",
        "comments": "Workout comments",
        "exercises": [
            {
                "name": "Exercise Name",
                "description": "Exercise description",
                "category": "Bodyweight/Strength/etc.",
                "repetitions": 12,
                "sets": 3,
                "weight": 50
            }
        ]
      }
      ```

- **Update Workout**
    - Endpoint: `/workouts/<workout_id>`
    - Method: `PUT`
    - Request body:
      ```json
      {
        "date": "YYYY-MM-DD",
        "comments": "Updated comments"
      }
      ```

- **Delete Workout**
    - Endpoint: `/workouts/<workout_id>`
    - Method: `DELETE`

- **List Workouts**
    - Endpoint: `/workouts`
    - Method: `GET`

### Report Generation
- **Generate Report**
    - Endpoint: `/workouts/report`
    - Method: `GET`
    - Response: 
      ```json
      {
        "total_workouts": 2,
        "workouts": [
          {
            "date": "YYYY-MM-DD",
            "comments": "Workout comments",
            "exercises": [
              {
                "name": "Exercise Name",
                "category": "Exercise category",
                "repetitions": 12,
                "sets": 3,
                "weight": 50
              }
            ]
          }
        ]
      }
      ```

## Testing

To run the tests:
```bash
pytest
```

All the tests for authentication and workout management are included in the `tests/` directory.

## Using cURL for Testing

Here are some example cURL commands to interact with the API:

- **Sign Up:**
    ```bash
    curl -X POST "http://127.0.0.1:5000/signup" -H "Content-Type: application/json" -d "{"email": "testuser@example.com", "password": "testpassword"}"
    ```

- **Log In:**
    ```bash
    curl -X POST "http://127.0.0.1:5000/login" -H "Content-Type: application/json" -d "{"email": "testuser@example.com", "password": "testpassword"}"
    ```

- **Create Workout:**
    ```bash
    curl -X POST "http://127.0.0.1:5000/workouts" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{"date": "2024-10-01", "comments": "Morning workout", "exercises": [{"name": "Push-up", "description": "Chest exercise", "category": "Bodyweight", "repetitions": 15, "sets": 3, "weight": 0}]}"
    ```

- **Generate Report:**
    ```bash
    curl -X GET "http://127.0.0.1:5000/workouts/report" -H "Authorization: Bearer <TOKEN>"
    ```

Make sure to replace `<TOKEN>` with the actual JWT token returned from the login endpoint.

The idea for this workout tracker application is inspired by [Roadmap.sh](https://roadmap.sh/projects/fitness-workout-tracker).

## License

This project is licensed under the MIT License.
