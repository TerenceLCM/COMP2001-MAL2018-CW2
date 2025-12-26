# MAL2018 Information Management Retrieval CW2 (COMP2001)
Microservice implemented using FastAPI for managing hiking trails as part of COMP2001 CW2.

**ID:** BSCS2506052  
**Institution:** Peninsula College Georgetown  
**Programme:** BSc (Hons) Computer Science (Cyber Security)

## Prerequisites
- Python 3.9+
- SQL Server (CW2 schema must be created before running the API)

## How to Run:

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Start the API

```bash
uvicorn app.main:app --reload
```

3. API Access

- Base URL: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
