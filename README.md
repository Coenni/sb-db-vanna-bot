# Vanna AI Integration Application

A complete full-stack application that integrates Vanna AI for natural language to SQL queries. The application consists of an Angular frontend, Spring Boot backend, and a Python-based Vanna AI microservice.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Angular        │─────▶│  Spring Boot     │─────▶│  Vanna AI       │
│  Frontend       │      │  Backend         │      │  Microservice   │
│  (Port 4200)    │◀─────│  (Port 8080)     │◀─────│  (Port 5000)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                                             │
                                                             ▼
                         ┌──────────────────┐      ┌─────────────────┐
                         │  PostgreSQL      │      │  ChromaDB       │
                         │  Database        │      │  Vector Store   │
                         │  (Port 5432)     │      │                 │
                         └──────────────────┘      └─────────────────┘
```

## Features

### Frontend (Angular)
- **Train Page**: Interface for training the Vanna AI model with:
  - DDL (Data Definition Language) statements
  - Documentation and business context
  - SQL query examples with questions
- **Ask Page**: Interface for asking natural language questions and viewing:
  - Generated SQL queries
  - Query results in a table format
  - Error handling and loading states

### Backend (Spring Boot)
- RESTful API endpoints for frontend communication
- Proxy layer to Vanna AI microservice
- CORS configuration for cross-origin requests
- Comprehensive error handling and logging

### Vanna AI Microservice (Python/Flask)
- Integration with Vanna AI library
- OpenAI GPT integration for natural language processing
- ChromaDB for vector embeddings storage
- PostgreSQL database connectivity
- Training endpoints for DDL, documentation, and SQL examples
- Query generation and execution

## Prerequisites

- Docker and Docker Compose
- OpenAI API key (for Vanna AI)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Coenni/sb-db-vanna-bot.git
cd sb-db-vanna-bot
```

### 2. Configure Environment Variables

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432) with pre-populated sample data
- Vanna AI microservice (port 5000)
- Spring Boot backend (port 8080)
- Angular frontend (port 4200)

**Note:** The PostgreSQL database is automatically initialized with comprehensive sample e-commerce data including:
- 30 customers from 16 different countries
- 25 products across 5 categories (Electronics, Furniture, Office Supplies, Appliances, Accessories)
- 50 orders with various statuses (delivered, pending, processing, shipped, cancelled)
- Order history spanning several months for time-based analysis

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:4200
```

### 5. Initial Training

Before asking questions, you need to train the Vanna AI model:

1. Go to the **Train** page
2. Start with **DDL** tab and paste the database schema (sample tables are already created)
3. Optionally add **Documentation** to provide context
4. Add **SQL Examples** with question-answer pairs

Example DDL training (sample schema already in database):
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);
```

Example SQL training:
- Question: "What are the total sales by country?"
- SQL: `SELECT c.country, SUM(o.total_amount) as total_sales FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.country ORDER BY total_sales DESC;`

### 6. Ask Questions

Navigate to the **Ask** page and try questions like:
- "Show me total sales by country"
- "What are the top 5 best-selling products?"
- "List customers who haven't ordered in the last 30 days"
- "What's the average order value per customer?"
- "List all products in the Electronics category"
- "Show monthly sales trends for the last 6 months"
- "Which product category generates the most revenue?"
- "List all pending orders with customer details"
- "What's the total inventory value by category?"
- "Show customers from the USA who have spent more than $500"

## Development

### Running Individual Services

#### Frontend (Angular)
```bash
cd frontend
npm install
npm start
# Access at http://localhost:4200
```

#### Backend (Spring Boot)
```bash
cd backend
mvn spring-boot:run
# API available at http://localhost:8080
```

#### Vanna Service (Python)
```bash
cd vanna-service
pip install -r requirements.txt
python app.py
# Service available at http://localhost:5000
```

## API Documentation

### Backend Endpoints (Spring Boot)

#### Health Check
```
GET /api/health
```

#### Training Endpoints
```
POST /api/train/ddl
Body: { "ddl": "CREATE TABLE ..." }

POST /api/train/documentation
Body: { "documentation": "Table description..." }

POST /api/train/sql
Body: { "question": "...", "sql": "SELECT ..." }
```

#### Query Endpoint
```
POST /api/ask
Body: { "question": "How many users?" }

Response: {
  "success": true,
  "data": {
    "question": "How many users?",
    "sql": "SELECT COUNT(*) FROM users;",
    "results": [...],
    "columns": [...]
  }
}
```

### Vanna Service Endpoints (Python)

```
GET  /health
POST /train/ddl
POST /train/documentation
POST /train/sql
POST /ask
GET  /training-data
POST /remove-training-data
```

## Project Structure

```
.
├── frontend/                 # Angular application
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/  # Train and Ask components
│   │   │   ├── services/    # API service
│   │   │   └── ...
│   │   └── environments/    # Environment configs
│   ├── Dockerfile
│   └── nginx.conf
│
├── backend/                  # Spring Boot application
│   ├── src/
│   │   └── main/
│   │       └── java/com/vanna/backend/
│   │           ├── controller/  # REST controllers
│   │           ├── service/     # Business logic
│   │           ├── dto/         # Data transfer objects
│   │           └── config/      # Configuration
│   ├── pom.xml
│   └── Dockerfile
│
├── vanna-service/           # Vanna AI microservice
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml       # Docker orchestration
├── init-db.sql             # Database initialization
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Technologies Used

### Frontend
- Angular 17
- TypeScript
- RxJS
- CSS3

### Backend
- Spring Boot 3.2
- Java 17
- Maven
- Lombok

### Vanna Service
- Python 3.11
- Flask
- Vanna AI
- OpenAI API
- ChromaDB
- psycopg2

### Infrastructure
- Docker & Docker Compose
- PostgreSQL 16
- Nginx

## Troubleshooting

### Services not starting
```bash
# Check logs
docker-compose logs -f

# Check specific service
docker-compose logs -f vanna-service
```

### Database connection issues
```bash
# Restart PostgreSQL
docker-compose restart postgres

# Check PostgreSQL logs
docker-compose logs postgres
```

### OpenAI API errors
- Verify your API key in `.env`
- Check API quota and billing
- Ensure the key has proper permissions

### Frontend can't connect to backend
- Check CORS configuration in Spring Boot
- Verify environment URLs in `frontend/src/environments/`
- Ensure backend is running: `curl http://localhost:8080/api/health`

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes all data)
docker-compose down -v
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.