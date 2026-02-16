# Quick Start Guide

Get the Vanna AI application up and running in minutes!

## Choose Your Setup

- **🌐 Online Mode (OpenAI)** - Follow this guide
- **🔒 Offline Mode (Ollama)** - See [OFFLINE_SETUP.md](OFFLINE_SETUP.md) - No internet/API key required!

## Prerequisites

- Docker and Docker Compose installed on your machine
- **For Online Mode:** OpenAI API key (get one from https://platform.openai.com/api-keys)
- **For Offline Mode:** See [OFFLINE_SETUP.md](OFFLINE_SETUP.md)

## Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/Coenni/sb-db-vanna-bot.git
cd sb-db-vanna-bot

# Copy environment file
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Step 2: Start the Application

```bash
docker compose up -d
```

**What happens during startup:**
1. PostgreSQL starts and initializes with sample e-commerce data
2. Vanna service starts and **automatically trains itself** (first time only!)
   - Auto-discovers database schema
   - Trains with table structures
   - Loads business documentation
   - Adds 10+ SQL example queries
3. Backend and frontend services start

Wait for all services to start (about 2-3 minutes for first startup). You can check the status:

```bash
docker compose ps
```

All services should show as "running" or "healthy".

**Check auto-training logs:**
```bash
docker compose logs vanna-service | grep "TRAINING"
```

You should see:
```
STARTING AUTOMATIC INITIAL TRAINING
Auto-discovered 4 tables from database
INITIAL TRAINING COMPLETE!
```

## Step 3: Access the Application

Open your browser and navigate to:
```
http://localhost:4200
```

## Step 4: Ask Questions Immediately! 🎉

**NEW:** No manual training required! Vanna is already trained and ready to use.

1. Click on **Ask** in the navigation
2. Type a natural language question, for example:
   - "How many customers do we have?"
   - "Show me total sales by country"
   - "What are the top 5 best-selling products?"
   - "List all pending orders"
3. Click **Ask** or press Enter
4. View the generated SQL and results!

## Step 5: Optional - Add Custom Training

Want to add your own training data? You have two options:

### Option A: Use the Web Interface

1. Click on **Train** in the navigation
2. Add custom DDL, documentation, or SQL examples
3. Click the appropriate Train button

### Option B: Use train.http File

The repository includes `train.http` with 50+ ready-to-use training examples:

1. Open `train.http` in VS Code (with REST Client extension) or IntelliJ IDEA
2. Execute individual requests to add more training:
   - Additional DDL for new tables
   - More documentation for business context
   - Additional SQL examples for specific use cases

Example from train.http:
```http
### Train with custom SQL example
POST http://localhost:8080/api/train/sql
Content-Type: application/json

{
  "question": "Show customers who haven't ordered in 60 days",
  "sql": "SELECT c.name, c.email, MAX(o.order_date) as last_order FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id HAVING MAX(o.order_date) < NOW() - INTERVAL '60 days';"
}
```

## Pre-Loaded Sample Database

The application comes with comprehensive sample data:
- **30 customers** from 16 different countries
- **25 products** across 5 categories (Electronics, Furniture, Office Supplies, Appliances, Accessories)
- **50 orders** with various statuses (delivered, pending, processing, shipped, cancelled)
- **Order history** spanning several months

Try these sample questions:
- "Show me total sales by country"
- "What are the top 5 best-selling products?"
- "List customers who haven't ordered in the last 30 days"
- "What's the average order value per customer?"
- "Which product category generates the most revenue?"
- "Show customers from the USA who have spent more than $500"

## Stopping the Application

```bash
docker compose down
```

To stop and remove all data (including the database):
```bash
docker compose down -v
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker compose logs -f

# Check specific service
docker compose logs vanna-service
```

### Can't access the frontend
- Make sure port 4200 is not in use
- Check if the frontend container is running: `docker compose ps`
- Try accessing http://127.0.0.1:4200 instead

### API errors
- Verify your OpenAI API key is correct in `.env`
- Check your OpenAI account has credits
- Restart services: `docker compose restart`

### Database connection errors
```bash
# Restart PostgreSQL
docker compose restart postgres
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- Explore individual component READMEs:
  - [Frontend README](frontend/README.md)
  - [Backend README](backend/README.md)
  - [Vanna Service README](vanna-service/README.md)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs: `docker compose logs -f`
3. Open an issue on GitHub with details and error messages

Enjoy using Vanna AI! 🚀
