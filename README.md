# Agentic Travel Planner

An AI-powered travel planning application that researches destinations, generates personalized itineraries, and validates travel budgets using agentic AI workflows.

**Status:** In development. The FastAPI backend, Docker environment, and initial automated testing are implemented. AI workflows and the frontend are planned.

## Run the application

**Requirements:** Docker Desktop. No local Python installation is required when running the backend through Docker.

### 1. Clone the repository

```bash
git clone <repository-url>
cd agentic-travel-planner
```

The repository URL will be added after the first GitHub push.

### 2. Build and start the backend

Build the Docker image:

```bash
docker build -t agentic-travel-planner-backend ./backend
```

Start the container:

```bash
docker run -d \
  --name agentic-travel-planner-backend \
  -p 8000:8000 \
  agentic-travel-planner-backend
```

Open the API documentation:

http://localhost:8000/docs

The health endpoint is available at:

http://localhost:8000/health

Expected response:

```json
{
  "status": "ok"
}
```

The backend runs on Python 3.12 inside Docker, independently of the Python version installed on the host machine.

### 3. Run locally without Docker

Alternatively, run the backend directly using Python.

**Requirements:** Python 3.12 or newer.

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## Try it

The current implementation provides a health endpoint to verify that the backend is running.

Open:

http://localhost:8000/health

Or use curl:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "ok" }
```

Interactive API documentation is available through FastAPI's Swagger UI at http://localhost:8000/docs.

### Planned functionality

The completed application will allow users to:

- Enter a destination, travel dates, budget, and interests.
- Generate personalized day-by-day travel itineraries.
- Research attractions and activities using external tools.
- Estimate costs and validate itineraries against budget constraints.
- Automatically refine itineraries when constraints are not satisfied.
- Review and modify travel plans through an interactive web interface.

## Architecture and choices

The application is being developed as a full-stack system with a Python backend, an agentic AI workflow, and a TypeScript frontend.

### Current architecture

```text
HTTP Client
    |
    v
Uvicorn
    |
    v
FastAPI Backend
    |
    v
GET /health
    |
    v
JSON Response
```

The backend is packaged in a Docker image and runs as a non-root user.

### Planned architecture

```text
Next.js Frontend
       |
       v
FastAPI Backend
       |
       v
LangGraph Workflow
       |
       +--> Destination Research
       |         |
       |         v
       |      MCP Tools
       |
       +--> Itinerary Generation
       |         |
       |         v
       |      LLM
       |
       +--> Budget Validation
                 |
          +------+------+
          |             |
          v             v
        Valid       Needs Revision
          |             |
          |             +--> Itinerary Generation
          v
    Final Itinerary
          |
          v
    Next.js Frontend
```

### Technology choices

- **FastAPI** provides the REST API, request validation, and automatic API documentation.
- **Uvicorn** serves the FastAPI application using the ASGI interface.
- **Docker** provides a reproducible backend environment with Python 3.12.
- **pytest and HTTPX** support automated API testing.
- **LangChain (planned)** will handle LLM integration and structured model interactions.
- **LangGraph (planned)** will coordinate stateful planning workflows, conditional routing, and itinerary refinement.
- **MCP (planned)** will connect the application to external research tools.
- **Next.js and TypeScript (planned)** will provide the interactive frontend.
- **Tailwind CSS (planned)** will provide frontend styling.

LangGraph was selected because travel planning involves multiple dependent steps rather than a single LLM request. The workflow will be able to evaluate generated itineraries and revise them when necessary.

Redis, RabbitMQ, Kafka, and Kubernetes are intentionally excluded from the initial architecture. The application does not currently require distributed caching, message queues, event streaming, or container orchestration.

Additional infrastructure will only be introduced when justified by actual requirements.

## Project structure

```text
agentic-travel-planner/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_health.py
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
├── README.md
├── WORKLOG.md
└── .gitignore
```

The frontend and AI workflow modules will be added as development progresses.

## Limitations

- The application currently exposes only the backend health endpoint.
- LLM integration and itinerary generation are not yet implemented.
- Destination research and MCP integration are planned.
- Budget validation and automatic itinerary refinement are not yet implemented.
- The frontend is not yet available.
- Live attraction prices, opening hours, and availability will only be presented as verified when supported by reliable external data sources.
- The current Docker setup is intended for local development and does not include production deployment infrastructure.

As the application evolves, this section will document additional limitations related to AI accuracy, external APIs, cost estimation, and deployment.

## Testing

The backend uses pytest and FastAPI's TestClient.

An initial test checks that the `/health` endpoint returns HTTP 200 and the expected JSON response.

To run the tests:

```bash
cd backend
source .venv/bin/activate
python -m pytest -v
```

Additional tests will be introduced for itinerary generation, workflow transitions, budget validation, and external tool integration.

Implementation progress and technical decisions are recorded in [WORKLOG.md](WORKLOG.md).

## Stop or troubleshoot

### Stop the container

```bash
docker stop agentic-travel-planner-backend
```

### Restart the container

```bash
docker start agentic-travel-planner-backend
```

### View container logs

```bash
docker logs agentic-travel-planner-backend
```

### Check container status

```bash
docker ps -a
```

### Rebuild after backend changes

Stop and remove the existing container:

```bash
docker stop agentic-travel-planner-backend
docker rm agentic-travel-planner-backend
```

Rebuild and start the updated application:

```bash
docker build -t agentic-travel-planner-backend ./backend

docker run -d \
  --name agentic-travel-planner-backend \
  -p 8000:8000 \
  agentic-travel-planner-backend
```

### Docker daemon unavailable

If Docker reports that it cannot connect to the Docker daemon, ensure Docker Desktop is running.

### Port 8000 already in use

If another application is using port 8000, stop that application or map the container to a different host port:

```bash
docker run -d \
  --name agentic-travel-planner-backend \
  -p 8001:8000 \
  agentic-travel-planner-backend
```

The API will then be accessible at http://localhost:8001.

## Screenshots and demo

Screenshots and a video walkthrough will be added once the frontend and core AI functionality are implemented.
