# Twitter Clone Project

A minimal Twitter-style web application built with Flask and PostgreSQL, supporting user accounts, full-text search with RUM indexing, and Dockerized deployment.

---

##  Instructions

### 1. Build the Docker containers

```bash
docker-compose build

### 2. 2. Start the containers in detached mode
docker-compose up -d

### edit the environment file 
### edit the .env.dev file
FLASK_APP=project/__init__.py
FLASK_DEBUG=0
DATABASE_URL=postgresql://postgres:pass@db:5432/postgres
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/home/app/web

### 4. port forwarding 
ssh -L 1064:localhost:1064 your_username@your_server_ip


### 5 the app 
should be available to you at http://localhost:1064 
