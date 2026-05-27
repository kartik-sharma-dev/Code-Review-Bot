# Code Review Bot

A local AI-powered code review tool built with FastAPI. Paste your Python code via the web UI or hit the REST API directly — no cloud API, no data leaving your machine.

## Model

Uses **LLaMA 3** (`llama3`) running locally via **[Ollama](https://ollama.com)**. The model is downloaded and served entirely on your machine.

## Features

- Accepts Python code only (non-Python submissions are rejected)
- Reviews across 7 dimensions: Bugs, Indentation, Complexity, Readability, Performance, Security, and Structure
- Provides before/after fix snippets for every issue found
- REST API endpoint (`POST /review`) for programmatic use
- Fully offline — no API keys required

## Screenshots

<img width="1673" height="969" alt="image" src="https://github.com/user-attachments/assets/4ce43391-0b45-4efe-97be-710e2d85bad2" />

<img width="1697" height="936" alt="image" src="https://github.com/user-attachments/assets/b4b820ea-3cb4-43de-b622-286d8484dd7f" />



## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running locally
- LLaMA 3 model pulled via Ollama

## Setup

**1. Install Ollama and pull the model**

Download and install from [ollama.com](https://ollama.com), then:

```bash
ollama pull llama3
```

**2. Clone the repo**

```bash
git clone <your-repo-url>
cd code_review_bot
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Start Ollama (if not already running)**

```bash
ollama serve
```

**5. Run the app**

```bash
uvicorn app:app --reload
```

The app will open at `http://localhost:8000`.

## API

### `POST /review`

**Request**
```json
{ "code": "your python code here" }
```

**Response**
```json
{ "review": "structured review output..." }
```

**Example with curl**
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def foo():\n  pass"}'
```

Interactive API docs are available at `http://localhost:8000/docs`.

## Project Structure

```
code_review_bot/
├── app.py           # FastAPI app — routes and HTML UI
├── reviewer.py      # Ollama integration and review logic
├── requirements.txt
└── .gitignore
```
