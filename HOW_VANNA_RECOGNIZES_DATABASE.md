# How Vanna AI Recognizes Your Database Setup

This document explains how Vanna AI learns about and recognizes your database structure.

## Overview

Vanna AI needs TWO things to work properly:

1. **DATABASE CONNECTION** - To execute SQL queries
2. **SCHEMA KNOWLEDGE** - To generate correct SQL queries

## The Two-Step Process

### Step 1: Database Connection (Runtime)

When the Vanna service starts, it connects to PostgreSQL:

```python
# In app.py - connects Vanna to PostgreSQL
vn_instance.connect_to_postgres(
    host=DB_CONFIG['host'],
    dbname=DB_CONFIG['database'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    port=DB_CONFIG['port']
)
```

**What this does:**
- Establishes a connection to your PostgreSQL database
- Allows Vanna to execute generated SQL queries
- Enables Vanna to fetch query results

**What this does NOT do:**
- Does NOT teach Vanna about your table structures
- Does NOT tell Vanna what columns exist
- Does NOT explain table relationships

### Step 2: Schema Training (One-Time)

Vanna learns about your database structure through training:

#### A. Automatic Schema Discovery (Recommended)

On first startup, Vanna automatically:

1. **Queries information_schema** to discover actual tables:
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

2. **Reads column definitions** for each table:
   ```sql
   SELECT column_name, data_type, is_nullable, column_default
   FROM information_schema.columns
   WHERE table_name = 'customers';
   ```

3. **Generates DDL statements** from the discovered schema:
   ```sql
   CREATE TABLE customers (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100) NOT NULL UNIQUE,
       country VARCHAR(50) NOT NULL,
       ...
   );
   ```

4. **Trains Vanna** with the discovered schema:
   ```python
   vn_instance.train(ddl=discovered_ddl)
   ```

#### B. Manual DDL Training (Fallback)

If auto-discovery fails, predefined DDL is used from `initial_training.py`:

```python
DDL_TRAINING = [
    "CREATE TABLE customers (...)",
    "CREATE TABLE products (...)",
    "CREATE TABLE orders (...)",
    "CREATE TABLE order_items (...)"
]
```

#### C. Documentation Training

Teaches Vanna about business context:

```python
DOCUMENTATION_TRAINING = [
    "This is an e-commerce database...",
    "The customers table stores...",
    "Products are organized by category..."
]
```

#### D. SQL Example Training

Shows Vanna how to write queries:

```python
SQL_TRAINING = [
    {
        "question": "Show me total sales by country",
        "sql": "SELECT c.country, SUM(o.total_amount) ..."
    }
]
```

## How It All Works Together

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SERVICE STARTUP                                          │
│    - Load environment variables                             │
│    - Initialize Vanna instance                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DATABASE CONNECTION (app.py)                             │
│    vn_instance.connect_to_postgres(...)                     │
│    → Enables query execution                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CHECK FOR TRAINING DATA                                  │
│    if vn_instance.get_training_data() is empty:             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. AUTO-DISCOVER SCHEMA (initial_training.py)               │
│    - Query information_schema tables                        │
│    - Read column definitions                                │
│    - Generate CREATE TABLE statements                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. TRAIN VANNA                                              │
│    - Train with DDL (schema structure)                      │
│    - Train with documentation (business context)            │
│    - Train with SQL examples (query patterns)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. READY TO USE                                             │
│    Vanna now knows:                                         │
│    ✓ WHERE the database is (connection)                     │
│    ✓ WHAT tables exist (DDL training)                       │
│    ✓ WHAT the business context is (documentation)           │
│    ✓ HOW to write queries (SQL examples)                    │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### Enable/Disable Auto-Training

Set in `.env` file:

```bash
# Enable automatic training (default)
AUTO_TRAIN_ON_STARTUP=true

# Disable automatic training
AUTO_TRAIN_ON_STARTUP=false
```

### When Auto-Training Runs

- **First startup only** - When no training data exists
- **After clearing ChromaDB** - If vector store is reset
- **Never if data exists** - Prevents duplicate training

### Force Re-Training

To force re-training, clear the ChromaDB data:

```bash
# Stop services
docker-compose down

# Remove ChromaDB volume
docker volume rm sb-db-vanna-bot_vanna-chromadb

# Restart - will auto-train again
docker-compose up
```

## Training Data Storage

Training data is stored in ChromaDB (vector database):

- **Location**: `./chromadb/` (or Docker volume `vanna-chromadb`)
- **Persistence**: Survives container restarts
- **Format**: Vector embeddings of DDL, docs, and SQL examples

## Troubleshooting

### Vanna generates incorrect SQL

**Problem**: Table or column names are wrong

**Solution**: 
1. Check training data: `GET /api/training-data`
2. Verify schema matches actual database
3. Re-train if needed or clear ChromaDB and restart

### Vanna can't find tables

**Problem**: "Table 'xyz' does not exist"

**Solution**:
1. Verify database connection works
2. Check that auto-discovery ran: Look for "Auto-discovered X tables" in logs
3. Manually train with DDL if needed: `POST /api/train/ddl`

### Training doesn't run on startup

**Problem**: No training happens on first startup

**Solution**:
1. Check environment variable: `AUTO_TRAIN_ON_STARTUP=true`
2. Check logs for "Performing automatic initial training"
3. Verify no existing training data (check `/api/training-data`)

## Manual Training Alternative

If you prefer manual control, disable auto-training and use `train.http`:

1. Set `AUTO_TRAIN_ON_STARTUP=false` in `.env`
2. Use the requests in `train.http` to train manually
3. Execute DDL, documentation, and SQL training requests in order

## Summary

**Vanna recognizes your database through:**

1. ✅ **Connection** - Connects to PostgreSQL (configured in docker-compose.yml)
2. ✅ **Schema Discovery** - Auto-reads tables from information_schema
3. ✅ **DDL Training** - Learns table structures and relationships
4. ✅ **Documentation** - Understands business context
5. ✅ **SQL Examples** - Learns query patterns

This two-step approach (connection + training) ensures Vanna knows both WHERE your database is and WHAT it contains.
