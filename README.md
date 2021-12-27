# Product Delivery FastAPI

## What is fastAPI ?
FastAPI is a Web framework for developing RESTful APIs in Python. FastAPI is based on Pydantic and type hints to validate, serialize, and deserialize data, and automatically auto-generate OpenAPI documents. It fully supports asynchronous programming and can run with Uvicorn and Gunicorn.

### Install FastAPI
```
pip install "fastapi[all]"
```

You can also install it part by part.

This is what you would probably do once you want to deploy your application to production:

```
pip install fastapi
```
Also install uvicorn to work as the server:


```
pip install "uvicorn[standard]"
```

## what is uvicorn ?
Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools.

## What is pydentic model
You can think of models as similar to types in strictly typed languages, or as the requirements of a single endpoint in an API.


## Database connection
```
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```
## Run server 
```
uvicorn main:app --reload
```

# Project structure
## models:
All database related files

## schemas:
All pydentic model files

## routers
All end point define here
