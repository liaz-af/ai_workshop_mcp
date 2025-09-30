# AI Workshop API Service

This service provides an API interface for the AI Workshop functionality.

## Setup

1. Install the package in development mode:
```bash
pip install -e .
```

2. Set up environment variables:
Create a `.env` file in the root directory with:
```
AF_ONELINK_TOKEN=your_token_here
```

## Running the Service

Run the service using uvicorn:
```bash
uvicorn ai_workshop.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc` 