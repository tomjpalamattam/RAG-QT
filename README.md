
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

Embed Your Loal documents

<img width="1479" height="838" alt="2025-10-18-18:30:58" src="https://github.com/user-attachments/assets/66561c5d-f60a-4035-a9c3-ee459095c772" />

Ask Questions

<img width="1397" height="783" alt="2025-10-18-18:08:39" src="https://github.com/user-attachments/assets/bc02fcd0-2654-4a28-9249-7af5882b1843" />

Context Aware

<img width="1397" height="783" alt="2025-10-18-18:09:20" src="https://github.com/user-attachments/assets/a440fc23-ab9a-4b9d-957b-f16730a69773" />


