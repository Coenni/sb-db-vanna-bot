-- ============================================================================
-- PostgreSQL Database Initialization Script for Vanna AI Testing
-- ============================================================================
-- 
-- Purpose: This script automatically initializes a PostgreSQL database with 
-- sample e-commerce data for testing Vanna AI's natural language to SQL 
-- capabilities. The data includes customers, products, orders, and order items
-- with realistic relationships and variety for comprehensive testing.
--
-- Automatic Initialization: This script runs automatically when the PostgreSQL
-- container starts for the first time via docker-compose.
--
-- Example Vanna AI Test Queries:
-- - "Show me total sales by country"
-- - "What are the top 5 best-selling products?"
-- - "List customers who haven't ordered in the last 30 days"
-- - "What's the average order value per customer?"
-- - "Show monthly sales trends for the last 6 months"
-- - "Which product category generates the most revenue?"
-- - "List all pending orders with customer details"
-- - "What's the total inventory value by category?"
-- - "Show customers from the USA who have spent more than $500"
-- - "What's the most popular product in each country?"
-- ============================================================================

-- Drop existing tables if they exist (for clean reinstallation)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ============================================================================
-- Table: customers
-- Description: Stores customer information including geographic location
-- ============================================================================
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,  -- UNIQUE constraint automatically creates an index
    country VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: products
-- Description: Product catalog with categories, pricing, and inventory
-- ============================================================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: orders
-- Description: Customer orders with status tracking and timestamps
-- ============================================================================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    CONSTRAINT valid_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'))
);

-- ============================================================================
-- Table: order_items
-- Description: Line items for each order linking products to orders
-- ============================================================================
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT positive_quantity CHECK (quantity > 0)
);

-- ============================================================================
-- Sample Data: Customers (30 customers from various countries)
-- ============================================================================
INSERT INTO customers (name, email, country, city, created_at) VALUES
    ('John Smith', 'john.smith@email.com', 'USA', 'New York', '2023-06-15 10:30:00'),
    ('Emma Johnson', 'emma.j@email.com', 'UK', 'London', '2023-07-01 14:20:00'),
    ('Michael Brown', 'michael.b@email.com', 'Canada', 'Toronto', '2023-07-10 09:15:00'),
    ('Sophia Martinez', 'sophia.m@email.com', 'Spain', 'Madrid', '2023-07-15 16:45:00'),
    ('William Davis', 'william.d@email.com', 'USA', 'Los Angeles', '2023-08-01 11:00:00'),
    ('Olivia Garcia', 'olivia.g@email.com', 'Mexico', 'Mexico City', '2023-08-05 13:30:00'),
    ('James Wilson', 'james.w@email.com', 'Australia', 'Sydney', '2023-08-10 08:45:00'),
    ('Ava Anderson', 'ava.a@email.com', 'USA', 'Chicago', '2023-08-20 15:10:00'),
    ('Robert Taylor', 'robert.t@email.com', 'UK', 'Manchester', '2023-09-01 10:25:00'),
    ('Isabella Thomas', 'isabella.t@email.com', 'France', 'Paris', '2023-09-05 14:40:00'),
    ('David Moore', 'david.m@email.com', 'Germany', 'Berlin', '2023-09-10 09:30:00'),
    ('Mia Jackson', 'mia.j@email.com', 'Canada', 'Vancouver', '2023-09-15 16:20:00'),
    ('Joseph White', 'joseph.w@email.com', 'USA', 'Houston', '2023-09-20 11:50:00'),
    ('Charlotte Harris', 'charlotte.h@email.com', 'Netherlands', 'Amsterdam', '2023-10-01 13:15:00'),
    ('Daniel Martin', 'daniel.m@email.com', 'Italy', 'Rome', '2023-10-05 10:40:00'),
    ('Amelia Thompson', 'amelia.t@email.com', 'USA', 'Phoenix', '2023-10-10 15:30:00'),
    ('Matthew Lee', 'matthew.l@email.com', 'South Korea', 'Seoul', '2023-10-15 09:00:00'),
    ('Harper Walker', 'harper.w@email.com', 'Australia', 'Melbourne', '2023-10-20 14:25:00'),
    ('Christopher Hall', 'chris.h@email.com', 'UK', 'Birmingham', '2023-11-01 11:10:00'),
    ('Evelyn Allen', 'evelyn.a@email.com', 'USA', 'San Francisco', '2023-11-05 16:45:00'),
    ('Andrew Young', 'andrew.y@email.com', 'Canada', 'Montreal', '2023-11-10 10:20:00'),
    ('Abigail King', 'abigail.k@email.com', 'New Zealand', 'Auckland', '2023-11-15 13:50:00'),
    ('Joshua Wright', 'joshua.w@email.com', 'USA', 'Seattle', '2023-11-20 09:35:00'),
    ('Emily Scott', 'emily.s@email.com', 'Ireland', 'Dublin', '2023-11-25 15:15:00'),
    ('Ryan Green', 'ryan.g@email.com', 'USA', 'Boston', '2023-12-01 11:40:00'),
    ('Elizabeth Adams', 'elizabeth.a@email.com', 'Belgium', 'Brussels', '2023-12-05 14:05:00'),
    ('Daniel Baker', 'daniel.b@email.com', 'Sweden', 'Stockholm', '2023-12-10 10:50:00'),
    ('Sofia Nelson', 'sofia.n@email.com', 'USA', 'Miami', '2023-12-15 16:25:00'),
    ('Alexander Carter', 'alex.c@email.com', 'Switzerland', 'Zurich', '2023-12-20 12:30:00'),
    ('Victoria Mitchell', 'victoria.m@email.com', 'USA', 'Denver', '2024-01-05 09:45:00');

-- ============================================================================
-- Sample Data: Products (25 products across multiple categories)
-- ============================================================================
INSERT INTO products (name, category, price, stock_quantity, description, created_at) VALUES
    ('Premium Laptop Pro', 'Electronics', 1299.99, 45, 'High-performance laptop with 16GB RAM', '2023-06-01 10:00:00'),
    ('Wireless Mouse Elite', 'Electronics', 49.99, 250, 'Ergonomic wireless mouse with precision tracking', '2023-06-01 10:00:00'),
    ('Mechanical Keyboard RGB', 'Electronics', 129.99, 120, 'Gaming mechanical keyboard with RGB lighting', '2023-06-01 10:00:00'),
    ('4K Monitor 32"', 'Electronics', 599.99, 60, 'Ultra HD 4K monitor with HDR support', '2023-06-01 10:00:00'),
    ('USB-C Hub', 'Electronics', 39.99, 300, '7-in-1 USB-C hub with multiple ports', '2023-06-01 10:00:00'),
    ('Ergonomic Office Chair', 'Furniture', 349.99, 40, 'Premium ergonomic chair with lumbar support', '2023-06-15 10:00:00'),
    ('Standing Desk', 'Furniture', 499.99, 25, 'Electric height-adjustable standing desk', '2023-06-15 10:00:00'),
    ('Desk Lamp LED', 'Furniture', 59.99, 150, 'Adjustable LED desk lamp with touch control', '2023-06-15 10:00:00'),
    ('Bookshelf Oak', 'Furniture', 199.99, 30, '5-tier solid oak bookshelf', '2023-06-15 10:00:00'),
    ('Wireless Headphones', 'Electronics', 199.99, 180, 'Noise-cancelling Bluetooth headphones', '2023-07-01 10:00:00'),
    ('Smartphone Pro', 'Electronics', 899.99, 95, 'Latest flagship smartphone with 5G', '2023-07-01 10:00:00'),
    ('Tablet 10"', 'Electronics', 449.99, 110, 'High-resolution 10-inch tablet', '2023-07-01 10:00:00'),
    ('External SSD 1TB', 'Electronics', 149.99, 200, 'Portable solid-state drive with fast transfer', '2023-07-15 10:00:00'),
    ('Webcam HD', 'Electronics', 79.99, 140, '1080p webcam with autofocus', '2023-07-15 10:00:00'),
    ('Office Desk Mat', 'Office Supplies', 29.99, 220, 'Large desk mat with smooth surface', '2023-08-01 10:00:00'),
    ('Notebook Set', 'Office Supplies', 19.99, 350, 'Set of 5 premium notebooks', '2023-08-01 10:00:00'),
    ('Pen Collection', 'Office Supplies', 24.99, 400, 'Luxury pen collection set', '2023-08-01 10:00:00'),
    ('Coffee Maker', 'Appliances', 89.99, 75, 'Programmable coffee maker with timer', '2023-08-15 10:00:00'),
    ('Blender Pro', 'Appliances', 129.99, 55, 'High-speed blender with multiple settings', '2023-08-15 10:00:00'),
    ('Air Purifier', 'Appliances', 199.99, 45, 'HEPA air purifier for large rooms', '2023-09-01 10:00:00'),
    ('Smart Watch', 'Electronics', 299.99, 130, 'Fitness tracking smartwatch', '2023-09-15 10:00:00'),
    ('Portable Charger', 'Electronics', 34.99, 280, '20000mAh portable power bank', '2023-09-15 10:00:00'),
    ('Cable Organizer', 'Office Supplies', 14.99, 450, 'Desk cable management system', '2023-10-01 10:00:00'),
    ('Monitor Stand', 'Furniture', 44.99, 160, 'Adjustable monitor stand with storage', '2023-10-01 10:00:00'),
    ('Laptop Backpack', 'Accessories', 69.99, 190, 'Water-resistant laptop backpack', '2023-10-15 10:00:00');

-- ============================================================================
-- Sample Data: Orders (50 orders with varied dates and statuses)
-- ============================================================================
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
    (1, '2023-08-15 10:30:00', 1349.98, 'delivered'),
    (2, '2023-08-20 14:15:00', 649.98, 'delivered'),
    (3, '2023-09-01 09:45:00', 499.99, 'delivered'),
    (4, '2023-09-10 16:20:00', 229.97, 'delivered'),
    (5, '2023-09-15 11:30:00', 1299.99, 'delivered'),
    (6, '2023-09-20 13:45:00', 899.99, 'delivered'),
    (7, '2023-09-25 10:15:00', 449.99, 'delivered'),
    (8, '2023-10-01 15:30:00', 949.98, 'delivered'),
    (9, '2023-10-05 09:20:00', 349.99, 'delivered'),
    (10, '2023-10-10 14:40:00', 759.97, 'delivered'),
    (11, '2023-10-15 11:10:00', 1299.99, 'delivered'),
    (12, '2023-10-20 16:25:00', 199.99, 'delivered'),
    (13, '2023-10-25 10:50:00', 299.99, 'delivered'),
    (14, '2023-11-01 13:15:00', 549.98, 'delivered'),
    (15, '2023-11-05 09:35:00', 1899.98, 'delivered'),
    (16, '2023-11-10 15:20:00', 449.99, 'delivered'),
    (17, '2023-11-15 11:45:00', 899.99, 'delivered'),
    (18, '2023-11-20 14:30:00', 199.99, 'delivered'),
    (19, '2023-11-25 10:15:00', 349.99, 'delivered'),
    (20, '2023-12-01 16:40:00', 1499.98, 'delivered'),
    (21, '2023-12-05 09:25:00', 499.99, 'delivered'),
    (22, '2023-12-10 13:50:00', 649.98, 'delivered'),
    (23, '2023-12-15 11:20:00', 299.99, 'delivered'),
    (24, '2023-12-20 15:35:00', 759.97, 'delivered'),
    (25, '2023-12-25 10:45:00', 449.99, 'delivered'),
    (1, '2024-01-05 14:20:00', 599.99, 'delivered'),
    (3, '2024-01-08 09:30:00', 349.99, 'delivered'),
    (5, '2024-01-12 16:15:00', 899.99, 'delivered'),
    (7, '2024-01-15 11:40:00', 229.97, 'delivered'),
    (9, '2024-01-18 13:25:00', 1299.99, 'delivered'),
    (11, '2024-01-22 10:10:00', 499.99, 'delivered'),
    (13, '2024-01-25 15:50:00', 749.98, 'delivered'),
    (15, '2024-01-28 09:35:00', 199.99, 'delivered'),
    (2, '2024-02-01 14:45:00', 549.98, 'shipped'),
    (4, '2024-02-03 11:20:00', 1299.99, 'shipped'),
    (6, '2024-02-05 16:30:00', 349.99, 'shipped'),
    (8, '2024-02-07 10:15:00', 899.99, 'shipped'),
    (10, '2024-02-09 13:40:00', 449.99, 'processing'),
    (12, '2024-02-11 09:25:00', 599.99, 'processing'),
    (14, '2024-02-13 15:10:00', 1499.98, 'processing'),
    (16, '2024-02-14 11:35:00', 299.99, 'processing'),
    (18, '2024-02-15 14:20:00', 749.98, 'pending'),
    (20, '2024-02-15 10:50:00', 199.99, 'pending'),
    (22, '2024-02-15 16:15:00', 649.98, 'pending'),
    (24, '2024-02-16 09:40:00', 449.99, 'pending'),
    (26, '2024-02-16 13:25:00', 899.99, 'pending'),
    (28, '2024-02-16 11:10:00', 1299.99, 'pending'),
    (30, '2024-01-10 15:30:00', 349.99, 'cancelled'),
    (25, '2024-01-20 10:45:00', 199.99, 'cancelled'),
    (27, '2024-02-01 14:20:00', 599.99, 'cancelled');

-- ============================================================================
-- Sample Data: Order Items (detailed line items for all orders)
-- ============================================================================
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    -- Order 1: Customer 1
    (1, 1, 1, 1299.99),
    (1, 2, 1, 49.99),
    -- Order 2: Customer 2
    (2, 4, 1, 599.99),
    (2, 2, 1, 49.99),
    -- Order 3: Customer 3
    (3, 7, 1, 499.99),
    -- Order 4: Customer 4
    (4, 10, 1, 199.99),
    (4, 15, 1, 29.99),
    -- Order 5: Customer 5
    (5, 1, 1, 1299.99),
    -- Order 6: Customer 6
    (6, 11, 1, 899.99),
    -- Order 7: Customer 7
    (7, 12, 1, 449.99),
    -- Order 8: Customer 8
    (8, 6, 1, 349.99),
    (8, 4, 1, 599.99),
    -- Order 9: Customer 9
    (9, 6, 1, 349.99),
    -- Order 10: Customer 10
    (10, 21, 1, 299.99),
    (10, 12, 1, 449.99),
    (10, 5, 1, 39.99),
    (10, 14, 1, 79.99),
    -- Order 11: Customer 11
    (11, 1, 1, 1299.99),
    -- Order 12: Customer 12
    (12, 20, 1, 199.99),
    -- Order 13: Customer 13
    (13, 21, 1, 299.99),
    -- Order 14: Customer 14
    (14, 18, 1, 89.99),
    (14, 12, 1, 449.99),
    (14, 5, 1, 39.99),
    -- Order 15: Customer 15
    (15, 1, 1, 1299.99),
    (15, 4, 1, 599.99),
    -- Order 16: Customer 16
    (16, 12, 1, 449.99),
    -- Order 17: Customer 17
    (17, 11, 1, 899.99),
    -- Order 18: Customer 18
    (18, 20, 1, 199.99),
    -- Order 19: Customer 19
    (19, 6, 1, 349.99),
    -- Order 20: Customer 20
    (20, 1, 1, 1299.99),
    (20, 10, 1, 199.99),
    -- Order 21: Customer 21
    (21, 7, 1, 499.99),
    -- Order 22: Customer 22
    (22, 4, 1, 599.99),
    (22, 2, 1, 49.99),
    -- Order 23: Customer 23
    (23, 21, 1, 299.99),
    -- Order 24: Customer 24
    (24, 10, 1, 199.99),
    (24, 21, 1, 299.99),
    (24, 3, 1, 129.99),
    (24, 13, 1, 149.99),
    -- Order 25: Customer 25
    (25, 12, 1, 449.99),
    -- Order 26: Customer 1
    (26, 4, 1, 599.99),
    -- Order 27: Customer 3
    (27, 6, 1, 349.99),
    -- Order 28: Customer 5
    (28, 11, 1, 899.99),
    -- Order 29: Customer 7
    (29, 10, 1, 199.99),
    (29, 15, 1, 29.99),
    -- Order 30: Customer 9
    (30, 1, 1, 1299.99),
    -- Order 31: Customer 11
    (31, 7, 1, 499.99),
    -- Order 32: Customer 13
    (32, 4, 1, 599.99),
    (32, 13, 1, 149.99),
    -- Order 33: Customer 15
    (33, 20, 1, 199.99),
    -- Order 34: Customer 2
    (34, 18, 1, 89.99),
    (34, 12, 1, 449.99),
    (34, 5, 1, 39.99),
    -- Order 35: Customer 4
    (35, 1, 1, 1299.99),
    -- Order 36: Customer 6
    (36, 6, 1, 349.99),
    -- Order 37: Customer 8
    (37, 11, 1, 899.99),
    -- Order 38: Customer 10
    (38, 12, 1, 449.99),
    -- Order 39: Customer 12
    (39, 4, 1, 599.99),
    -- Order 40: Customer 14
    (40, 1, 1, 1299.99),
    (40, 10, 1, 199.99),
    -- Order 41: Customer 16
    (41, 21, 1, 299.99),
    -- Order 42: Customer 18
    (42, 10, 1, 199.99),
    (42, 18, 1, 89.99),
    (42, 12, 1, 449.99),
    (42, 5, 1, 39.99),
    -- Order 43: Customer 20
    (43, 20, 1, 199.99),
    -- Order 44: Customer 22
    (44, 4, 1, 599.99),
    (44, 2, 1, 49.99),
    -- Order 45: Customer 24
    (45, 12, 1, 449.99),
    -- Order 46: Customer 26
    (46, 11, 1, 899.99),
    -- Order 47: Customer 28
    (47, 1, 1, 1299.99),
    -- Order 48: Customer 30 (cancelled)
    (48, 6, 1, 349.99),
    -- Order 49: Customer 25 (cancelled)
    (49, 20, 1, 199.99),
    -- Order 50: Customer 27 (cancelled)
    (50, 4, 1, 599.99);

-- ============================================================================
-- Create indexes for better query performance
-- ============================================================================
CREATE INDEX idx_customers_country ON customers(country);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- ============================================================================
-- End of initialization script
-- ============================================================================
