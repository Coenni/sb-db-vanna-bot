# Vanna AI Integration Application

A complete full-stack application that integrates Vanna AI for natural language to SQL queries. The application consists of an Angular frontend, Spring Boot backend, and a Python-based Vanna AI microservice.

## 🚀 Quick Start

**Just want to get started?** See [QUICKSTART.md](QUICKSTART.md)

**Want offline operation?** See [OFFLINE_SETUP.md](OFFLINE_SETUP.md) - No internet required!

**Want to validate everything works?** See [END_TO_END_VALIDATION.md](END_TO_END_VALIDATION.md)

**Key Features:**
- ✅ **Auto-training on first startup** - No manual setup required!
- ✅ **Pre-loaded sample data** - 30 customers, 25 products, 50 orders
- ✅ **Ready to use immediately** - Ask questions right away
- ✅ **Extensible** - Add custom training via UI or train.http
- ✅ **Offline mode supported** - Use local LLMs via Ollama (no API key, no internet!)

## LLM Provider Options

Choose your preferred LLM provider:

| Provider | Internet | API Key | Cost | Setup Difficulty |
|----------|----------|---------|------|------------------|
| **OpenAI** (default) | Required | Required | Pay-per-use | Easy |
| **Ollama** (offline) | Not required | Not required | Free | Medium |

See [OFFLINE_SETUP.md](OFFLINE_SETUP.md) for complete offline setup instructions.

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
- **Dual LLM support:** OpenAI (cloud) or Ollama (offline)
- ChromaDB for vector embeddings storage
- PostgreSQL database connectivity
- Training endpoints for DDL, documentation, and SQL examples
- Query generation and execution

## Prerequisites

### Required
- Docker and Docker Compose

### LLM Provider (choose one)

**Option 1: OpenAI (Default)**
- OpenAI API key (get from https://platform.openai.com/api-keys)
- Internet connection required
- Pay-per-use pricing

**Option 2: Ollama (Offline)**
- Ollama installed (https://ollama.ai)
- No API key required
- No internet required (after initial setup)
- Completely free
- See [OFFLINE_SETUP.md](OFFLINE_SETUP.md) for details

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
- Vanna AI microservice (port 5000) with **automatic initial training**
- Spring Boot backend (port 8080)
- Angular frontend (port 4200)

**Note:** The PostgreSQL database is automatically initialized with comprehensive sample e-commerce data including:
- 30 customers from 16 different countries
- 25 products across 5 categories (Electronics, Furniture, Office Supplies, Appliances, Accessories)
- 50 orders with various statuses (delivered, pending, processing, shipped, cancelled)
- Order history spanning several months for time-based analysis

**First-Time Training:** On first startup, Vanna AI will automatically:
1. Discover your database schema from PostgreSQL
2. Train itself with table structures and relationships
3. Load business documentation and sample queries
4. Be ready to answer questions immediately

See [HOW_VANNA_RECOGNIZES_DATABASE.md](./HOW_VANNA_RECOGNIZES_DATABASE.md) for details on how Vanna learns your database setup.

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:4200
```

### 5. Initial Training

**🎉 NEW: Automatic Training on First Startup!**

Vanna AI now automatically trains itself when the service starts for the first time. No manual training is required!

**What happens automatically:**
1. Vanna discovers your database schema from PostgreSQL
2. Learns table structures and relationships
3. Loads business documentation and context
4. Trains with 10+ example SQL queries
5. Ready to answer questions immediately!

**Manual Training (Optional)**

If you prefer manual control or want to add custom training:

**Option 1: Using the Web Interface**
1. Go to the **Train** page
2. Start with **DDL** tab and paste the database schema (sample tables are already created)
3. Optionally add **Documentation** to provide context
4. Add **SQL Examples** with question-answer pairs

**Option 2: Using the train.http File (Recommended for Quick Setup)**

The repository includes a `train.http` file with ready-to-use training examples:

1. Open `train.http` in VS Code (with REST Client extension) or IntelliJ IDEA
2. Execute the requests in order:
   - Start with DDL training requests (database schema)
   - Add documentation for business context
   - Train with SQL examples (15+ question-answer pairs)
3. Test your training by executing the "Ask" requests at the end of the file

The `train.http` file includes:
- 5 DDL training examples
- 7 documentation examples
- 15 SQL question-answer pairs
- 8 ready-to-test questions
- Complete usage documentation

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
- SQL: `SELECT c.country, SUM(o.total_amount) as total_sales FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.status != 'cancelled' GROUP BY c.country ORDER BY total_sales DESC;`

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

### Quick Start with train.http

The easiest way to train the model and test the API is using the included `train.http` file:

```bash
# Open train.http in VS Code (with REST Client extension) or IntelliJ IDEA
# Execute requests sequentially to train the model with sample data
```

See the `train.http` file for 30+ ready-to-use API examples.

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
├── init-db.sql             # Database initialization with sample data
├── train.http              # API training examples (30+ requests)
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