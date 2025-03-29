# Gen AI Analytics - Mini Data Query Simulation Engine

A lightweight backend service that simulates a **Gen AI-powered** data query system.

## 🚀 Features  
✅ Accepts natural language queries  
✅ Converts queries into pseudo-SQL  
✅ Simulates AI-powered data insights  
✅ Basic authentication included  
✅ Simple REST API for easy integration  

## 📌 1. Installation & Setup  
### 🔹 Prerequisites  
- Python 3.x  
- pip installed  

### 🔹 Install Dependencies  
```sh
pip install -r requirements.txt
```

### 🔹 Run the Server  
```sh
uvicorn main:app --reload
```
(Default: Runs on `http://127.0.0.1:8000/`)  

## 📌 2. API Endpoints  

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/query` | Accepts a natural language query and returns SQL + mock results |
| `POST` | `/explain` | Breaks down how a specific query would be processed |
| `POST` | `/validate` | Checks if a query is valid and suggests alternatives if not |
| `POST` | `/login` | Returns an authentication token for API access |


## 📌 3. Example Requests (Using `curl`)  

### 🔹 **Authentication**
```sh
curl -X POST "http://127.0.0.1:8000/login?username=demo&password=password"
```

### 🔹 **Send a Query**  
```sh
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Authorization: Bearer mysecuretoken" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me total sales"}'
```

### 🔹 **Explain a Query**  
```sh
curl -X POST "http://127.0.0.1:8000/explain" \
  -H "Authorization: Bearer mysecuretoken" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me sales by month"}'
```

### 🔹 **Validate a Query**  
```sh
curl -X POST "http://127.0.0.1:8000/validate" \
  -H "Authorization: Bearer mysecuretoken" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me customer count"}'
```
## 📌 7. Example Supported Queries

The system currently supports the following types of natural language queries:

- "Show me total sales"
- "What's the customer count?"
- "Show sales by month"
- "Show sales by product"
- "Show sales by region"
- "Who are our top customers?"
- "What's the product performance?"
- "Show me sales trend over time"


## 📌 4. Deployment  
You can deploy this backend on **Render, Railway, or Heroku**.  

Example (Deploying on Railway):  
1. Create a **new project** on [Railway](https://railway.app/).  
2. Link your GitHub repository.  
3. Set environment variables (if needed).  
4. Deploy! 🎉  

## 📌 5. Authentication  
This API uses **Bearer Token authentication**. Include the token in the `Authorization` header like this:  
```
Authorization: Bearer your-secret-token
```

## 📌 6. Tech Stack  
- **Language:** Python  
- **Framework:** FastAPI  
- **Database:** SQLite (Mock data)  

## 📌 7. Contributors  
👤 **Unnati**  
📧 Email: unnatisinghrajawat@gmail.com  
