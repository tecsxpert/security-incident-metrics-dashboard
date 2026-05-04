\# Security Incident Metrics Dashboard



\## Overview

Spring Boot backend for tracking security incidents with JWT auth, Redis caching, email alerts and Docker support.



\## Tech Stack

\- Java 17 and Spring Boot 3.2.5

\- PostgreSQL 15 and Redis 7

\- Docker and Docker Compose

\- JWT Authentication

\- JaCoCo 81% test coverage



\## Prerequisites

\- Java 17+

\- Maven 3.9+

\- Docker Desktop



\## Setup

1\. git clone https://github.com/Jennifercinthiya/security-incident-metrics-dashboard.git

2\. cd security-incident-metrics-dashboard/backend

3\. mvn clean package -DskipTests

4\. cd ..

5\. docker-compose up --build



\## API Endpoints

\- POST /auth/login - Public

\- GET /api/incidents - USER, ADMIN

\- POST /api/incidents - ADMIN

\- GET /api/incidents/{id} - USER, ADMIN

\- PUT /api/incidents/{id} - ADMIN

\- DELETE /api/incidents/{id} - ADMIN



\## Services

\- Backend API: http://localhost:8080

\- Swagger UI: http://localhost:8080/swagger-ui/index.html

\- MailHog: http://localhost:8025

\- Adminer: http://localhost:8081



\## Default Users

\- admin / admin123 - ADMIN

\- user / user123 - USER



\## Test Coverage

\- 25 tests passing

\- 81% JaCoCo coverage

