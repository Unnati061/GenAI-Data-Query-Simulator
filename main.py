from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import sqlite3
import random
from datetime import datetime, timedelta
import json
from database import init_db
import re







# Initialize the FastAPI app
app = FastAPI(
    title="Gen AI Analytics API",
    description="A lightweight backend service that simulates a Gen AI-powered data query system",
    version="1.0.0"
)

# Set up security
security = HTTPBearer()

# Dummy API Key (Replace with a secure method in production)
API_KEY = "mysecuretoken"

# Initialize the database at app startup
@app.on_event("startup")
def startup_event():
    init_db()

# Authentication Function
def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Token")

# Define request model
class QueryRequest(BaseModel):
    query: str

# Simulated database connection function
def connect_db():
    return sqlite3.connect("database.db")


# Convert natural language query to pseudo-SQL
def convert_to_sql(natural_query: str):
    # Normalize query
    query = natural_query.lower().strip()
    query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation

    # Sales queries
    if "total sales" in query or "sum of sales" in query:
        return "SELECT SUM(amount) FROM sales;"
    elif "sales by" in query and "month" in query:
        return "SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM sales GROUP BY month;"
    elif "sales by" in query and "product" in query:
        return "SELECT product_name, SUM(amount) FROM sales GROUP BY product_name;"
    elif "sales by" in query and "region" in query:
        return "SELECT region, SUM(amount) FROM sales GROUP BY region;"

    # Customer queries
    elif "customer count" in query or "number of customers" in query:
        return "SELECT COUNT(*) FROM customers;"
    elif "customer distribution by region" in query:
        return "SELECT region, COUNT(*) FROM customers GROUP BY region;"
    elif "top customers" in query or "biggest customers" in query:
        return "SELECT customer_name, SUM(amount) FROM sales GROUP BY customer_name ORDER BY SUM(amount) DESC LIMIT 10;"

    # Product queries
    elif "best selling product" in query or "top product" in query:
        return "SELECT product_name, SUM(amount) AS total_sales FROM sales GROUP BY product_name ORDER BY total_sales DESC LIMIT 1;"
    elif "product performance" in query:
        return "SELECT product_name, SUM(amount) AS total_sales FROM sales GROUP BY product_name ORDER BY total_sales DESC;"

    # Time-based queries
    elif "trend" in query or "sales over time" in query:
        return "SELECT date, SUM(amount) FROM sales GROUP BY date ORDER BY date;"

    # Average sales queries
    elif "average sales per customer" in query:
        return "SELECT AVG(total_sales) FROM (SELECT customer_id, SUM(amount) AS total_sales FROM sales GROUP BY customer_id);"

    # Fallback
    else:
        return "Invalid Query"

    
def execute_query(query: str):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



def generate_mock_data(sql_query: str):
    """Generate realistic mock data based on the SQL query"""
    
    # Total sales query
    if "SELECT SUM(amount) FROM sales" in sql_query and "GROUP BY" not in sql_query:
        return {
            "result": [{"total_sales": random.randint(500000, 2000000)}],
            "metadata": {
                "columns": ["total_sales"],
                "types": ["numeric"],
                "query_time_ms": random.randint(50, 200)
            }
        }
    
    # Sales by month
    elif "GROUP BY month" in sql_query:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        return {
            "result": [
                {"month": month, "total": random.randint(50000, 200000)} 
                for month in months
            ],
            "metadata": {
                "columns": ["month", "total"],
                "types": ["string", "numeric"],
                "query_time_ms": random.randint(50, 200)
            }
        }
    
    # Customer count
    elif "COUNT(*) FROM customers" in sql_query and "GROUP BY" not in sql_query:
        return {
            "result": [{"customer_count": random.randint(1000, 5000)}],
            "metadata": {
                "columns": ["customer_count"],
                "types": ["numeric"],
                "query_time_ms": random.randint(30, 100)
            }
        }
    
    # Top customers
    elif "customer_name" in sql_query and "ORDER BY" in sql_query:
        customers = ["Acme Corp", "TechGiant", "MegaRetail", "GlobalServices", "InnoSolutions"]
        return {
            "result": [
                {"customer_name": cust, "total_spend": random.randint(10000, 100000)} 
                for cust in customers
            ],
            "metadata": {
                "columns": ["customer_name", "total_spend"],
                "types": ["string", "numeric"],
                "query_time_ms": random.randint(50, 200)
            }
        }
    
    # Time trends
    elif "date" in sql_query and "GROUP BY date" in sql_query:
        base_date = datetime.now()
        dates = [(base_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
        return {
            "result": [
                {"date": date, "amount": random.randint(5000, 15000)} 
                for date in dates
            ],
            "metadata": {
                "columns": ["date", "amount"],
                "types": ["date", "numeric"],
                "query_time_ms": random.randint(50, 200)
            }
        }
    
    # Default case
    else:
        return {
            "result": [{"message": "No data available for this query type"}],
            "metadata": {
                "columns": ["message"],
                "types": ["string"],
                "query_time_ms": random.randint(10, 50)
            }
        }

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

@app.post("/query")
def process_query(request: QueryRequest, credentials: HTTPAuthorizationCredentials = Depends(authenticate)):
    """Process a natural language query and return SQL + results"""
    try:
        # Convert to SQL
        sql_query = convert_to_sql(request.query)
        
        # Validate query
        if sql_query == "Invalid Query":
            raise HTTPException(status_code=400, detail="Unsupported query format")
            
        # Generate mock results
        results = generate_mock_data(sql_query)
        
        # Return response
        return {
            "query": request.query,
            "sql_equivalent": sql_query,
            "results": results["result"],
            "metadata": results["metadata"],
            "success": True
        }
    except Exception as e:
        return {
            "query": request.query,
            "success": False,
            "error": str(e)
        }

@app.post("/explain")
def explain_query(request: QueryRequest, credentials: HTTPAuthorizationCredentials = Depends(authenticate)):
    """Explain how a query would be processed"""
    sql_query = convert_to_sql(request.query)
    
    if sql_query == "Invalid Query":
        return {
            "query": request.query,
            "valid": False,
            "explanation": "This query format is not supported. Try asking about sales, customers, or products."
        }
    
    # Simulate AI explanation of the query
    explanation_steps = [
        "1. Analyzed natural language query for intent",
        "2. Identified key entities (e.g., 'sales', 'customers', 'products')",
        "3. Determined aggregation type (e.g., sum, count, average)",
        "4. Generated SQL query",
        "5. Executed against database"
    ]
    
    query_type = "aggregate" if "SUM" in sql_query or "COUNT" in sql_query else "detail"
    entities = []
    if "sales" in sql_query:
        entities.append("sales")
    if "customers" in sql_query:
        entities.append("customers")
    if "products" in sql_query:
        entities.append("products")
    
    return {
        "query": request.query,
        "sql_equivalent": sql_query,
        "query_type": query_type,
        "entities_analyzed": entities,
        "processing_steps": explanation_steps,
        "valid": True
    }

@app.post("/validate")
def validate_query(request: QueryRequest, credentials: HTTPAuthorizationCredentials = Depends(authenticate)):
    """Validate if a query can be processed"""
    sql_query = convert_to_sql(request.query)
    is_valid = sql_query != "Invalid Query"
    
    if is_valid:
        return {
            "query": request.query,
            "valid": True,
            "supports": [
                "Conversion to SQL",
                "Data retrieval",
                "Result formatting"
            ]
        }
    else:
        suggested_queries = [
            "Show me total sales",
            "What's the customer count by region?",
            "Show sales trend over time",
            "Who are our top customers?"
        ]
        
        return {
            "query": request.query,
            "valid": False,
            "reason": "Query format not supported or ambiguous",
            "suggested_queries": suggested_queries
        }

# Add a simple login endpoint for authentication
@app.post("/login")
async def login(username: str = "demo", password: str = "password"):
    """Simple login endpoint to get authentication token"""
    if username == "demo" and password == "password":
        return {"access_token": API_KEY, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
