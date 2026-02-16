# Vanna AI Microservice

Python-based microservice that integrates with Vanna AI for natural language to SQL conversion.

## Features

- Train model with DDL, documentation, and SQL examples
- Generate SQL queries from natural language questions
- Execute queries and return results
- Integration with OpenAI GPT models
- ChromaDB for vector embeddings storage
- PostgreSQL database connectivity

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key

### Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the service:
```bash
python app.py
```

The service will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

### Training Endpoints

#### Train with DDL
```
POST /train/ddl
Content-Type: application/json

{
  "ddl": "CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100));"
}
```

#### Train with Documentation
```
POST /train/documentation
Content-Type: application/json

{
  "documentation": "The users table stores customer information..."
}
```

#### Train with SQL Examples
```
POST /train/sql
Content-Type: application/json

{
  "question": "How many active users are there?",
  "sql": "SELECT COUNT(*) FROM users WHERE status = 'active';"
}
```

### Query Endpoint

#### Ask a Question
```
POST /ask
Content-Type: application/json

{
  "question": "How many users do we have?"
}

Response:
{
  "success": true,
  "question": "How many users do we have?",
  "sql": "SELECT COUNT(*) FROM users;",
  "results": [{"count": 42}],
  "columns": ["count"]
}
```

## Configuration

Environment variables (see `.env.example`):

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `CHROMADB_PATH`: Path for ChromaDB storage (default: ./chromadb)
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: vanna_db)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password (default: postgres)
- `PORT`: Service port (default: 5000)

## Docker

Build and run with Docker:

```bash
docker build -t vanna-service .
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key vanna-service
```
