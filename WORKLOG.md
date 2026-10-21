# Work log

## Project planning

- Defined the goal of building an AI-powered travel planner that generates personalized itineraries based on destinations, budgets, trip duration, and user interests.
- Selected FastAPI for the backend and Next.js with TypeScript for the planned frontend.
- Selected LangChain for LLM integration, LangGraph for agentic workflow orchestration, and MCP for external tool integration.
- Planned a workflow consisting of destination research, itinerary generation, budget validation, and conditional refinement.
- Decided to introduce technologies incrementally and only when they provide a clear architectural benefit.
- Deferred Redis, RabbitMQ, Kafka, and Kubernetes because the initial application does not require distributed caching, message queues, event streaming, or container orchestration.

## Repository setup

- Created the `agentic-travel-planner` project directory.
- Initialized a Git repository and configured `main` as the default branch.
- Created the initial backend structure with separate application and test directories.
- Added `README.md` and `WORKLOG.md` for project documentation and development tracking.
- Configured `.gitignore` to exclude virtual environments, generated files, IDE settings, and environment variables.
- Verified that Git ignores the local Python virtual environment.

## Python environment

- Created and activated a Python virtual environment using Python 3.14.
- Installed FastAPI, Uvicorn, pytest, and HTTPX.
- Generated `requirements.txt` to record the installed dependencies.
- Selected Python 3.12 for the Docker environment to provide a consistent runtime independently of the locally installed Python version.

## Backend setup

- Created the FastAPI application in `backend/app/main.py`.
- Configured the application title, description, and version.
- Implemented a `GET /health` endpoint returning `{"status":"ok"}`.
- Selected Uvicorn as the ASGI server, consistent with the approach used in the previous Solvigo project.
- Started the backend locally using Uvicorn.
- Verified that the health endpoint returns the expected response.
- Confirmed that FastAPI automatically generates interactive API documentation through Swagger UI.

## Docker setup

- Created a Dockerfile based on `python:3.12-slim`.
- Configured the container working directory and Python environment variables.
- Installed backend dependencies from `requirements.txt`.
- Configured a non-root user to run the application.
- Configured Uvicorn to serve FastAPI on port 8000.
- Added `.dockerignore` to exclude unnecessary files from the Docker build context.
- Encountered a Docker daemon connection error because Docker Desktop was not running.
- Started Docker Desktop and confirmed that the Docker daemon was available.
- Encountered a missing Dockerfile error during the initial build.
- Created the Dockerfile in the backend directory and successfully built the Docker image.
- Started the backend container and verified that `/health` returns `{"status":"ok"}`.
- Configured an explicit container name instead of using Docker's automatically generated names.
- Removed the `--rm` flag to preserve stopped containers in Docker Desktop.
- Configured detached execution using `-d` to run the container in the background.

## Automated testing

- Added pytest and HTTPX as testing dependencies.
- Created `backend/tests/test_health.py`.
- Implemented a test using FastAPI's `TestClient`.
- Added assertions for HTTP status 200 and the expected JSON response.
- Automated test execution result to be confirmed.

## Documentation

- Created a README describing the project goals, features, and planned architecture.
- Documented implemented and planned technologies separately.
- Added instructions for running the backend locally and through Docker.
- Documented the reasoning behind FastAPI, Uvicorn, and Docker.
- Documented the decision to avoid unnecessary infrastructure during the initial development phase.
- Established this work log to track implementation progress alongside Git commits.

## GitHub setup

- Pending: Create the initial Git commit.
- Pending: Create a public GitHub repository.
- Pending: Push the project to the `main` branch.
