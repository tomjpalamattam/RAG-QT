
# QT RAG Project

A desktop application with Retrieval-Augmented Generation (RAG) capabilities, featuring a QT frontend and Python backend server(fastapi).

## Setup Instructions

### 1. Install UV Package Manager
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Python Virtual Environment
```
uv venv --python 3.12
```

### 3. Activate Virtual Environment
**On Linux/Mac:**
```
source .venv/bin/activate
```

**On Windows:**
```cmd
.venv\Scripts\activate
```

### 4. Install Python Dependencies
```
uv pip install -r requirements.txt
```

## Running the Application

### Starting the RAG Server
1. Navigate to the rag_server directory:
```bash
cd rag_server
```

2. Run the main.py file:
```bash
python main.py
```
The API server will start on http://localhost:8000

### Starting the QT Application
1. Navigate to the QT directory:
```bash
cd QT
```

2. Build and run the QT application using CMake:
```
mkdir build && cd build
cmake ..
make
./app
```
# Features

Embed Your Local Documents
Privately index PDFs, docs, and notes—no cloud required.

<img width="1520" height="885" alt="2025-10-19-22:24:15" src="https://github.com/user-attachments/assets/b39408fa-bae1-4ce8-b8ea-18730239dc89" />

Ask Questions
Query in plain English and get precise, source-linked answers.

<img width="1362" height="788" alt="2025-10-19-22:18:51" src="https://github.com/user-attachments/assets/6ad41204-2c47-4027-89be-439d8f9741b2" />


Context-Aware
Understands prior turns to keep answers on topic.

<img width="1362" height="788" alt="2025-10-19-22:20:10" src="https://github.com/user-attachments/assets/105378af-e537-43ee-8c23-02872e94405e" />


SQL-Backed Chat History (Session IDs)
Persist conversations per session for reliable, resumable threads.

<img width="1427" height="829" alt="2025-10-19-22:24:48" src="https://github.com/user-attachments/assets/bd23aa25-2afa-49de-91d0-8bf07195bc6e" />
<img width="1362" height="788" alt="2025-10-19-22:20:24" src="https://github.com/user-attachments/assets/12acd91f-6310-4412-b4b9-a2fe94bbfad2" />



---

## Docker Setup

This project includes a preconfigured **Docker Compose** setup to run the backend server in an isolated environment.

### Requirements

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/)

---

### Build and Run

To start the backend server, run the following command in the project root:

```bash
docker compose up --build
```

This will:

* Build the Docker image using the included `Dockerfile`
* Start the backend service defined in `compose.yaml`
* Expose the API on port **8000**

Once running, the API is available at:
👉 [http://localhost:8000](http://localhost:8000)

---

### Mounting Your Local Documents

By default, the container mounts the following local directory:

```yaml
services:
  ragqt:
    build:
      context: .
      dockerfile: ./Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - "${HOME}/Documents/Docs:/app/user_docs"
```

This means:

* Your **local folder** `${HOME}/Documents/Docs`
  is accessible **inside the container** at `/app/user_docs`.

You can change this to point to any folder on your system.
For example:

```yaml
volumes:
  - "/path/to/your/custom/folder:/app/user_docs"
```

---

### Using the Mounted Folder in the App

When embedding documents, always use `user_docs` in the directory path


---

### Stop the Container

To stop the running container:

```bash
docker compose down
```

To rebuild from scratch (for example, after editing dependencies or Dockerfile):

```bash
docker compose build --no-cache
docker compose up
```

---


## Notes
This application is based on langchain, qdrant, deepseek, sqlite and huggingface.
You should create a .env file in the rag_server/.env (you can see .env-example file)

