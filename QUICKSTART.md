# Quick Start Guide

Get the Vanna AI application up and running in minutes!

## Prerequisites

- Docker and Docker Compose installed on your machine
- OpenAI API key (get one from https://platform.openai.com/api-keys)

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

Wait for all services to start (about 1-2 minutes). You can check the status:

```bash
docker compose ps
```

All services should show as "running" or "healthy".

## Step 3: Access the Application

Open your browser and navigate to:
```
http://localhost:4200
```

## Step 4: Train the Model

Before asking questions, you need to train Vanna AI about your database:

1. Click on **Train** in the navigation
2. Select the **DDL** tab
3. Paste this sample DDL (or use your own):

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. Click **Train DDL**
5. Wait for success confirmation

You can also add:
- **Documentation**: Context about what the table stores
- **SQL Examples**: Question-SQL pairs to improve accuracy

Example SQL training:
- Question: "How many active users are there?"
- SQL: `SELECT COUNT(*) FROM users WHERE status = 'active';`

## Step 5: Ask Questions

1. Click on **Ask** in the navigation
2. Type a natural language question, for example:
   - "How many users are there?"
   - "Show me all active users"
   - "What is the total count of users by status?"
3. Click **Ask** or press Enter
4. View the generated SQL and results!

## Sample Database

The application comes with a pre-populated sample database including:
- Users table
- Products table
- Orders table
- Order items table

Try these sample questions:
- "How many products are in the Electronics category?"
- "Show me all users with their total order amounts"
- "What are the top 5 most expensive products?"
- "List all completed orders"

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
