
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
<img width="1036" height="510" alt="2025-10-17-04:21:21" src="https://github.com/user-attachments/assets/e7ff0062-a51d-4c50-bad3-0dca261ae219" />
<img width="1254" height="636" alt="2025-10-17-04:21:56" src="https://github.com/user-attachments/assets/01dde054-ad61-4595-bcbc-999c5f7c81a5" />
<img width="1313" height="653" alt="2025-10-17-04:22:18" src="https://github.com/user-attachments/assets/b3eef233-0990-4496-b05c-74a8e881e2b5" />
