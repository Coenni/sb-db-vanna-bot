"""
Initial Training Data for Vanna AI

This module contains the initial training data that will be automatically loaded
when the Vanna AI service starts for the first time with no existing training data.

Vanna AI recognizes your database setup through TWO mechanisms:
1. DATABASE CONNECTION: Vanna connects to PostgreSQL to execute queries
2. SCHEMA TRAINING: Vanna learns the table structures, relationships, and business logic

The training includes:
1. Database DDL (schema definitions) - Teaches Vanna about table structures
2. Business documentation (context and metadata) - Provides business context
3. SQL examples (question-answer pairs) - Shows Vanna how to write queries
4. Auto-discovered schema (optional) - Directly reads schema from connected database

HOW VANNA RECOGNIZES YOUR DATABASE:
- Connection (app.py): vn_instance.connect_to_postgres() → Enables query execution
- DDL Training (this file): vn_instance.train(ddl=...) → Teaches table structures
- Auto-discovery (this file): Queries information_schema → Learns actual database schema
"""

import logging
import psycopg2

logger = logging.getLogger(__name__)

# ============================================================================
# 1. DDL TRAINING DATA (Database Schema)
# ============================================================================

DDL_TRAINING = [
    # Customers table
    """CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        country VARCHAR(50) NOT NULL,
        city VARCHAR(100),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );""",
    
    # Products table
    """CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        description TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );""",
    
    # Orders table
    """CREATE TABLE orders (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER NOT NULL REFERENCES customers(id),
        order_date TIMESTAMP NOT NULL,
        total_amount DECIMAL(10, 2) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'pending',
        CONSTRAINT valid_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'))
    );""",
    
    # Order items table
    """CREATE TABLE order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL REFERENCES orders(id),
        product_id INTEGER NOT NULL REFERENCES products(id),
        quantity INTEGER NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL,
        CONSTRAINT positive_quantity CHECK (quantity > 0)
    );"""
]

# ============================================================================
# 2. DOCUMENTATION TRAINING DATA (Business Context)
# ============================================================================

DOCUMENTATION_TRAINING = [
    """This is an e-commerce database tracking customers, products, orders, and order details. 
    Customers can place multiple orders, and each order can contain multiple products. 
    We track order status throughout the fulfillment process. 
    Sales are analyzed by country, product category, and time period.""",
    
    """The customers table stores customer information including their name, email, country, and city. 
    Each customer has a unique email address. The created_at field tracks when the customer was registered.""",
    
    """The products table contains the product catalog with categories (Electronics, Furniture, 
    Office Supplies, Appliances, Accessories), pricing information, and current stock quantities. 
    Products are organized by category to help with inventory management and sales analysis.""",
    
    """The orders table tracks customer orders with different statuses: pending (newly placed), 
    processing (being prepared), shipped (in transit), delivered (completed), and cancelled. 
    Each order is linked to a customer and has a total amount and order date.""",
    
    """Customer locations are important for sales analysis. The database includes customers from 
    16 different countries including USA, UK, Canada, Germany, France, Spain, Italy, and others. 
    Use the country field for geographic sales analysis.""",
]

# ============================================================================
# 3. SQL TRAINING DATA (Question-Answer Pairs)
# ============================================================================

SQL_TRAINING = [
    {
        "question": "How many customers do we have?",
        "sql": "SELECT COUNT(*) as customer_count FROM customers;"
    },
    {
        "question": "Show me total sales by country",
        "sql": """SELECT c.country, SUM(o.total_amount) as total_sales 
                  FROM orders o 
                  JOIN customers c ON o.customer_id = c.id 
                  WHERE o.status != 'cancelled' 
                  GROUP BY c.country 
                  ORDER BY total_sales DESC;"""
    },
    {
        "question": "What are the top 5 best-selling products?",
        "sql": """SELECT p.name, SUM(oi.quantity) as total_sold 
                  FROM order_items oi 
                  JOIN products p ON oi.product_id = p.id 
                  GROUP BY p.id, p.name 
                  ORDER BY total_sold DESC 
                  LIMIT 5;"""
    },
    {
        "question": "What's the average order value per customer?",
        "sql": """SELECT c.name, AVG(o.total_amount) as avg_order_value 
                  FROM customers c 
                  JOIN orders o ON c.id = o.customer_id 
                  GROUP BY c.id, c.name 
                  ORDER BY avg_order_value DESC;"""
    },
    {
        "question": "List all products in the Electronics category",
        "sql": """SELECT name, price, stock_quantity 
                  FROM products 
                  WHERE category = 'Electronics' 
                  ORDER BY price DESC;"""
    },
    {
        "question": "Show me the last 10 orders",
        "sql": """SELECT o.id, c.name as customer_name, o.order_date, o.total_amount, o.status 
                  FROM orders o 
                  JOIN customers c ON o.customer_id = c.id 
                  ORDER BY o.order_date DESC 
                  LIMIT 10;"""
    },
    {
        "question": "List all pending orders with customer details",
        "sql": """SELECT o.id, c.name, c.email, o.order_date, o.total_amount 
                  FROM orders o 
                  JOIN customers c ON o.customer_id = c.id 
                  WHERE o.status = 'pending' 
                  ORDER BY o.order_date;"""
    },
    {
        "question": "Which product category generates the most revenue?",
        "sql": """SELECT p.category, SUM(oi.quantity * oi.unit_price) as total_revenue 
                  FROM order_items oi 
                  JOIN products p ON oi.product_id = p.id 
                  JOIN orders o ON oi.order_id = o.id 
                  WHERE o.status != 'cancelled' 
                  GROUP BY p.category 
                  ORDER BY total_revenue DESC;"""
    },
    {
        "question": "What's the total inventory value by category?",
        "sql": """SELECT category, SUM(price * stock_quantity) as inventory_value 
                  FROM products 
                  GROUP BY category 
                  ORDER BY inventory_value DESC;"""
    },
    {
        "question": "Show customers from the USA who have spent more than $500",
        "sql": """SELECT c.name, c.email, SUM(o.total_amount) as total_spent 
                  FROM customers c 
                  JOIN orders o ON c.id = o.customer_id 
                  WHERE c.country = 'USA' AND o.status != 'cancelled' 
                  GROUP BY c.id, c.name, c.email 
                  HAVING SUM(o.total_amount) > 500 
                  ORDER BY total_spent DESC;"""
    }
]

# ============================================================================
# AUTO-DISCOVERY: Read actual schema from connected database
# ============================================================================

def get_database_schema_from_db(db_config):
    """
    Auto-discover the actual database schema by querying information_schema.
    
    This function connects to the PostgreSQL database and retrieves the actual
    table structures, which provides Vanna with real-time schema information.
    
    Args:
        db_config: Dictionary with database connection parameters
        
    Returns:
        list: List of CREATE TABLE statements discovered from the database
    """
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Get all tables in public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        ddl_statements = []
        
        logger.info(f"Auto-discovering schema for {len(tables)} tables: {', '.join(tables)}")
        
        for table in tables:
            # Get column information
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' 
                AND table_name = %s
                ORDER BY ordinal_position;
            """, (table,))
            
            columns = cursor.fetchall()
            
            # Build simplified CREATE TABLE statement
            col_defs = []
            for col_name, data_type, max_len, nullable, default in columns:
                col_def = f"{col_name} {data_type.upper()}"
                
                if max_len:
                    col_def += f"({max_len})"
                
                if nullable == 'NO':
                    col_def += " NOT NULL"
                
                if default and not default.startswith('nextval'):
                    col_def += f" DEFAULT {default}"
                
                col_defs.append(col_def)
            
            ddl = f"CREATE TABLE {table} (\n    " + ",\n    ".join(col_defs) + "\n);"
            ddl_statements.append(ddl)
            logger.info(f"  ✓ Discovered schema for table: {table}")
        
        cursor.close()
        conn.close()
        
        return ddl_statements
        
    except Exception as e:
        logger.warning(f"Could not auto-discover database schema: {str(e)}")
        return []


# ============================================================================
# TRAINING FUNCTION
# ============================================================================

def perform_initial_training(vn_instance, db_config=None, use_auto_discovery=True):
    """
    Perform initial training of the Vanna AI model.
    
    This function trains the model with:
    1. Database DDL (schema) - either predefined or auto-discovered
    2. Business documentation
    3. SQL question-answer pairs
    
    HOW VANNA RECOGNIZES YOUR DATABASE:
    - The database connection (already established in app.py) allows Vanna to execute queries
    - The DDL training teaches Vanna about table structures and relationships
    - Auto-discovery reads the actual schema from information_schema (most accurate)
    - Documentation provides business context and domain knowledge
    - SQL examples show Vanna how to construct queries for your specific use cases
    
    Args:
        vn_instance: The Vanna instance to train
        db_config: Database configuration dict (for auto-discovery)
        use_auto_discovery: If True, try to discover schema from actual database
        
    Returns:
        tuple: (success: bool, message: str, counts: dict)
    """
    try:
        counts = {
            'ddl': 0,
            'documentation': 0,
            'sql': 0,
            'auto_discovered': 0
        }
        
        logger.info("=" * 80)
        logger.info("STARTING AUTOMATIC INITIAL TRAINING")
        logger.info("=" * 80)
        
        # 1. Try auto-discovery first (most accurate for actual database)
        ddl_to_train = []
        if use_auto_discovery and db_config:
            logger.info("Attempting to auto-discover database schema from connected database...")
            discovered_ddl = get_database_schema_from_db(db_config)
            if discovered_ddl:
                ddl_to_train = discovered_ddl
                counts['auto_discovered'] = len(discovered_ddl)
                logger.info(f"✓ Auto-discovered {len(discovered_ddl)} table schemas from database")
            else:
                logger.info("Auto-discovery failed, falling back to predefined DDL")
                ddl_to_train = DDL_TRAINING
        else:
            ddl_to_train = DDL_TRAINING
        
        # 2. Train with DDL (auto-discovered or predefined)
        logger.info("Training with DDL (database schema)...")
        for ddl in ddl_to_train:
            try:
                vn_instance.train(ddl=ddl)
                counts['ddl'] += 1
                # Extract table name for logging
                table_name = ddl.split('TABLE')[1].split('(')[0].strip() if 'TABLE' in ddl else 'schema'
                logger.info(f"  ✓ Trained DDL {counts['ddl']}/{len(ddl_to_train)}: {table_name}")
            except Exception as e:
                logger.warning(f"  ✗ Failed to train DDL: {str(e)[:100]}")
        
        # 3. Train with documentation
        logger.info("Training with documentation (business context)...")
        for doc in DOCUMENTATION_TRAINING:
            try:
                vn_instance.train(documentation=doc)
                counts['documentation'] += 1
                logger.info(f"  ✓ Trained documentation {counts['documentation']}/{len(DOCUMENTATION_TRAINING)}")
            except Exception as e:
                logger.warning(f"  ✗ Failed to train documentation: {str(e)[:100]}")
        
        # 4. Train with SQL examples
        logger.info("Training with SQL examples (question-answer pairs)...")
        for example in SQL_TRAINING:
            try:
                vn_instance.train(question=example['question'], sql=example['sql'])
                counts['sql'] += 1
                logger.info(f"  ✓ Trained SQL example {counts['sql']}/{len(SQL_TRAINING)}: {example['question'][:50]}")
            except Exception as e:
                logger.warning(f"  ✗ Failed to train SQL example: {str(e)[:100]}")
        
        logger.info("=" * 80)
        logger.info(f"INITIAL TRAINING COMPLETE!")
        if counts['auto_discovered'] > 0:
            logger.info(f"  - Schema auto-discovered: {counts['auto_discovered']} tables")
        logger.info(f"  - DDL trained: {counts['ddl']}/{len(ddl_to_train)}")
        logger.info(f"  - Documentation trained: {counts['documentation']}/{len(DOCUMENTATION_TRAINING)}")
        logger.info(f"  - SQL examples trained: {counts['sql']}/{len(SQL_TRAINING)}")
        logger.info(f"  - Total training items: {sum(counts.values())}")
        logger.info("")
        logger.info("Vanna now recognizes your database through:")
        logger.info("  1. Database connection (PostgreSQL at configured host)")
        logger.info("  2. Schema knowledge (table structures and relationships)")
        logger.info("  3. Business context (from documentation)")
        logger.info("  4. Query patterns (from SQL examples)")
        logger.info("=" * 80)
        
        success = sum(counts.values()) > 0
        message = f"Initial training completed: {counts['ddl']} DDL, {counts['documentation']} docs, {counts['sql']} SQL examples"
        
        return success, message, counts
        
    except Exception as e:
        error_msg = f"Error during initial training: {str(e)}"
        logger.error(error_msg)
        return False, error_msg, {'ddl': 0, 'documentation': 0, 'sql': 0, 'auto_discovered': 0}


def should_perform_initial_training(vn_instance, force=False):
    """
    Check if initial training should be performed.
    
    Args:
        vn_instance: The Vanna instance to check
        force: If True, perform training regardless of existing data
        
    Returns:
        bool: True if training should be performed, False otherwise
    """
    if force:
        logger.info("Force training flag is set - will perform initial training")
        return True
    
    try:
        # Check if any training data exists
        training_data = vn_instance.get_training_data()
        
        if not training_data or len(training_data) == 0:
            logger.info("No existing training data found - will perform initial training")
            return True
        else:
            logger.info(f"Found {len(training_data)} existing training items - skipping initial training")
            return False
            
    except Exception as e:
        logger.warning(f"Error checking training data: {str(e)}")
        # If we can't check, err on the side of not training to avoid duplicates
        return False
