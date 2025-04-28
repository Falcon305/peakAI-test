# Take-Home Assignment: Cognitive Assessment API


A Flask-based RESTful API for cognitive assessments through journal text analysis. The application analyzes journal entries using a simplified LIWC (Linguistic Inquiry and Word Count) algorithm to generate scores based on linguistic patterns.

## Features

- User authentication with JWT tokens
- Journal entry submission and analysis
- LIWC-based text analysis
- Score retrieval for journal entries
- API documentation with Swagger UI

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Documentation**: Swagger UI
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:

```bash
git clone git@github.com:Falcon305/peakAI-test.git
cd peakAI-test
```

2. Start the application using Docker Compose:

```bash
docker-compose up --build
```

This will:
- Build the Docker images
- Start the PostgreSQL database
- Initialize the database tables
- Start the Flask application on port 5000

### Accessing the Application

- API: http://localhost:5000
- Swagger Documentation: http://localhost:5000/api/docs

## API Documentation

### Authentication

#### Register a new user

**Swagger UI:**
Navigate to `/api/docs` and use the `/users` POST endpoint.

**cURL:**
```bash
curl -X POST \
  http://localhost:5000/users \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

#### Login

**Swagger UI:**
Navigate to `/api/docs` and use the `/login` POST endpoint.

**cURL:**
```bash
curl -X POST \
  http://localhost:5000/login \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

Response will include a JWT token that you should use for authenticated endpoints:
```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Journal Endpoints

#### Submit a Journal Entry

**Swagger UI:**
Navigate to `/api/docs` and use the `/journals` POST endpoint.

**cURL:**
```bash
curl -X POST \
  http://localhost:5000/journals \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "I am feeling happy today, but I was sad yesterday."
  }'
```

Response:
```json
{
  "journal_id": 1,
  "score": {
    "categories": {
      "positive_emotion": 1,
      "negative_emotion": 1
    },
    "total": 2
  }
}
```

#### Get Journals for Current User

**Swagger UI:**
Navigate to `/api/docs` and use the `/journals` GET endpoint.

**cURL:**
```bash
curl -X GET \
  http://localhost:5000/journals \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

#### Get Score for a Journal Entry

**Swagger UI:**
Navigate to `/api/docs` and use the `/journals/{id}/score` GET endpoint.

**cURL:**
```bash
curl -X GET \
  http://localhost:5000/journals/1/score \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

### Health Check

**Swagger UI:**
Navigate to `/api/docs` and use the `/health` GET endpoint.

**cURL:**
```bash
curl -X GET http://localhost:5000/health
```

## Testing

### Running Tests

Run the tests inside the Docker container:

```bash
docker-compose exec web pytest
```

### Test Coverage

To run tests with coverage:

```bash
docker-compose exec web pytest --cov=app
```

## Development

### Database Migrations

When making changes to the database schema, you need to re-initialize the database:

```bash
docker-compose exec web python init_db.py
```

### Hot Reloading

The development server has hot reloading enabled, so any changes to the Python files will automatically restart the server.

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues, ensure PostgreSQL is fully initialized:

```bash
docker-compose restart db
docker-compose exec web python init_db.py
```
