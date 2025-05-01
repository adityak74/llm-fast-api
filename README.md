# LLM FastAPI Server

A FastAPI-based server that provides an OpenAI-compatible API interface for local LLM models using llama.cpp.

## Features

- OpenAI-compatible API endpoints
- Support for local LLM models via llama.cpp
- Docker containerization for the API server
- Easy integration with existing OpenAI-based applications

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- llama.cpp installed locally
- A compatible GGUF model file (e.g., google_gemma-3-27b-it-Q4_K_M.gguf)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd llm-fast-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Install llama.cpp:

```bash
brew install llama.cpp
```

2. Place your GGUF model file in a convenient location (e.g., in the project root)

3. Start the llama.cpp server:

```bash
llama-server -m ./google_gemma-3-27b-it-Q4_K_M.gguf --host 127.0.0.1 --port 8080
```

4. Start the FastAPI server:

```bash
docker compose up
```

## API Endpoints

### Chat Completion

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google_gemma-3-27b-it",
    "messages": [
      {
        "role": "user",
        "content": "What is the capital of France?"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

### Direct llama.cpp API

```bash
curl -X POST http://localhost:8080/completion \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer not-needed" \
  -d '{
    "prompt": "Hello",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## Project Structure

```
llm-fast-api/
├── app/
│   ├── controllers/
│   │   └── chat_controller.py
│   ├── models/
│   │   └── chat.py
│   ├── services/
│   │   └── llm_service.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Configuration

### Environment Variables

- `LLM_SERVER_URL`: URL of the llama.cpp server (default: http://host.docker.internal:8080)

### Docker Configuration

The FastAPI server runs in a Docker container and communicates with the local llama.cpp server using `host.docker.internal`.

## Development

1. Make changes to the code
2. The FastAPI server will automatically reload due to the `--reload` flag
3. For changes to take effect in Docker, rebuild the container:

```bash
docker compose build
docker compose up
```

## Performance Considerations

- The llama.cpp server runs directly on your machine for better performance
- CPU-based inference may be slower than GPU-based solutions
- Adjust the `timeout` in `llm_service.py` if needed for longer responses

## License

[Your License Here]

## Contributing

[Your Contribution Guidelines Here]
