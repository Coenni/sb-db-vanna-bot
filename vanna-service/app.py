from flask import Flask, request, jsonify
from flask_cors import CORS
import vanna as vn
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
import os
import psycopg2
from dotenv import load_dotenv
import logging
from initial_training import should_perform_initial_training, perform_initial_training

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Custom Vanna class combining OpenAI and ChromaDB
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

# Initialize Vanna
vanna_config = {
    'api_key': os.getenv('OPENAI_API_KEY', ''),
    'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
    'path': os.getenv('CHROMADB_PATH', './chromadb'),
}

vn_instance = MyVanna(config=vanna_config)

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'vanna_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
}

def get_db_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return None

def connect_to_database():
    """Connect Vanna to the database."""
    try:
        vn_instance.connect_to_postgres(
            host=DB_CONFIG['host'],
            dbname=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        logger.info("Successfully connected Vanna to PostgreSQL database")
        return True
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        return False

# Connect to database on startup
connect_to_database()

# Perform automatic initial training if needed
def initialize_training():
    """
    Initialize Vanna training on first startup.
    
    This function checks if auto-training is enabled and if the model
    needs initial training (no existing training data). If both conditions
    are met, it performs automatic training with:
    
    1. Auto-discovered schema (reads actual database structure)
    2. Predefined DDL (fallback if auto-discovery fails)
    3. Business documentation
    4. SQL query examples
    
    HOW VANNA RECOGNIZES YOUR DATABASE:
    - Database Connection: vn_instance.connect_to_postgres() connects to PostgreSQL
    - Schema Training: Teaches Vanna about table structures and relationships
    - Auto-Discovery: Optionally reads actual schema from information_schema
    - Documentation: Provides business context and domain knowledge
    - SQL Examples: Shows Vanna how to write queries for your use cases
    """
    auto_train = os.getenv('AUTO_TRAIN_ON_STARTUP', 'true').lower() == 'true'
    
    if not auto_train:
        logger.info("Auto-training is disabled (AUTO_TRAIN_ON_STARTUP=false)")
        return
    
    logger.info("Checking if initial training is needed...")
    
    if should_perform_initial_training(vn_instance):
        logger.info("Performing automatic initial training...")
        # Pass DB_CONFIG to enable auto-discovery of actual database schema
        success, message, counts = perform_initial_training(vn_instance, db_config=DB_CONFIG, use_auto_discovery=True)
        
        if success:
            logger.info(f"✓ Auto-training successful: {message}")
        else:
            logger.error(f"✗ Auto-training failed: {message}")
    else:
        logger.info("Skipping auto-training - model already has training data")

# Run initial training check
initialize_training()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'vanna-ai-microservice'}), 200

@app.route('/train/ddl', methods=['POST'])
def train_ddl():
    """Train the model with DDL statements."""
    try:
        data = request.get_json()
        ddl = data.get('ddl')
        
        if not ddl:
            return jsonify({'error': 'DDL is required'}), 400
        
        vn_instance.train(ddl=ddl)
        logger.info(f"Successfully trained with DDL: {ddl[:100]}...")
        
        return jsonify({
            'success': True,
            'message': 'DDL trained successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error training DDL: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/train/documentation', methods=['POST'])
def train_documentation():
    """Train the model with documentation."""
    try:
        data = request.get_json()
        documentation = data.get('documentation')
        
        if not documentation:
            return jsonify({'error': 'Documentation is required'}), 400
        
        vn_instance.train(documentation=documentation)
        logger.info(f"Successfully trained with documentation: {documentation[:100]}...")
        
        return jsonify({
            'success': True,
            'message': 'Documentation trained successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error training documentation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/train/sql', methods=['POST'])
def train_sql():
    """Train the model with SQL query examples."""
    try:
        data = request.get_json()
        question = data.get('question')
        sql = data.get('sql')
        
        if not question or not sql:
            return jsonify({'error': 'Both question and SQL are required'}), 400
        
        vn_instance.train(question=question, sql=sql)
        logger.info(f"Successfully trained with Q&A pair: {question}")
        
        return jsonify({
            'success': True,
            'message': 'SQL example trained successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error training SQL: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Ask a question and get SQL query and results."""
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        logger.info(f"Processing question: {question}")
        
        # Generate SQL
        sql = vn_instance.generate_sql(question)
        logger.info(f"Generated SQL: {sql}")
        
        # Execute SQL and get results
        df = vn_instance.run_sql(sql)
        
        # Convert DataFrame to dict for JSON response
        results = df.to_dict(orient='records') if df is not None else []
        
        return jsonify({
            'success': True,
            'question': question,
            'sql': sql,
            'results': results,
            'columns': list(df.columns) if df is not None else []
        }), 200
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/training-data', methods=['GET'])
def get_training_data():
    """Get all training data."""
    try:
        training_data = vn_instance.get_training_data()
        return jsonify({
            'success': True,
            'data': training_data
        }), 200
    except Exception as e:
        logger.error(f"Error getting training data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/remove-training-data', methods=['POST'])
def remove_training_data():
    """Remove specific training data."""
    try:
        data = request.get_json()
        id_to_remove = data.get('id')
        
        if not id_to_remove:
            return jsonify({'error': 'ID is required'}), 400
        
        vn_instance.remove_training_data(id=id_to_remove)
        logger.info(f"Successfully removed training data with ID: {id_to_remove}")
        
        return jsonify({
            'success': True,
            'message': 'Training data removed successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error removing training data: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
