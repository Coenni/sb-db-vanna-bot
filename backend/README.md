# Spring Boot Backend

REST API backend that serves as a proxy between the Angular frontend and the Vanna AI microservice.

## Features

- RESTful API endpoints for training and querying
- Integration with Vanna AI microservice
- CORS configuration for frontend access
- Comprehensive error handling
- Request/response logging

## Local Development

### Prerequisites

- Java 17+
- Maven 3.6+

### Setup and Run

1. Build the application:
```bash
mvn clean install
```

2. Run the application:
```bash
mvn spring-boot:run
```

The API will be available at `http://localhost:8080`

## API Documentation

Base URL: `http://localhost:8080/api`

### Health Check
```
GET /api/health

Response:
{
  "success": true,
  "message": "Backend is healthy"
}
```

### Training Endpoints

#### Train with DDL
```
POST /api/train/ddl
Content-Type: application/json

{
  "ddl": "CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100));"
}
```

#### Train with Documentation
```
POST /api/train/documentation
Content-Type: application/json

{
  "documentation": "The users table stores customer information..."
}
```

#### Train with SQL Examples
```
POST /api/train/sql
Content-Type: application/json

{
  "question": "How many active users?",
  "sql": "SELECT COUNT(*) FROM users WHERE status = 'active';"
}
```

### Query Endpoint

#### Ask a Question
```
POST /api/ask
Content-Type: application/json

{
  "question": "How many users do we have?"
}

Response:
{
  "success": true,
  "message": "Question answered successfully",
  "data": {
    "question": "How many users do we have?",
    "sql": "SELECT COUNT(*) FROM users;",
    "results": [...],
    "columns": [...]
  }
}
```

#### Get Training Data
```
GET /api/training-data

Response:
{
  "success": true,
  "message": "Training data retrieved successfully",
  "data": {...}
}
```

## Configuration

Edit `src/main/resources/application.properties`:

```properties
# Server Configuration
server.port=8080

# Vanna Service URL
vanna.service.url=http://localhost:5000

# Frontend URL for CORS
frontend.url=http://localhost:4200
```

## Docker

Build and run with Docker:

```bash
docker build -t vanna-backend .
docker run -p 8080:8080 vanna-backend
```

## Project Structure

```
src/main/java/com/vanna/backend/
├── VannaBackendApplication.java  # Main application class
├── config/
│   └── WebConfig.java            # CORS and RestTemplate configuration
├── controller/
│   └── VannaController.java      # REST API endpoints
├── dto/
│   ├── ApiResponse.java          # Standard API response
│   ├── AskQuestionRequest.java   # Ask request DTO
│   ├── TrainDDLRequest.java      # DDL training request
│   ├── TrainDocumentationRequest.java
│   └── TrainSQLRequest.java      # SQL training request
└── service/
    └── VannaService.java         # Business logic, Vanna AI integration
```
