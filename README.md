# 🤖 LLM FastAPI Server for Gemma 3 27B (Apple Silicon Optimized)

A FastAPI-based server that provides an OpenAI-compatible API interface for local LLM models using [`llama.cpp`](https://github.com/ggerganov/llama.cpp), fully optimized for macOS with Metal GPU acceleration.

---

## 🚀 Features

- OpenAI-compatible API endpoints (`/v1/chat/completions`)
- Runs locally using `llama.cpp` on Apple Silicon (Metal support)
- Dockerized FastAPI proxy
- Easy integration with OpenAI SDKs and apps (e.g., LangChain, AutoGen, etc.)
- Direct `llama.cpp` completion endpoint exposed
- Log tailing and custom model aliases supported

---

## 🧱 Prerequisites

- macOS with Apple Silicon (M1/M2/M4)
- 64GB RAM for Gemma 3 27B
- Python 3.11+
- Docker + Docker Compose
- `brew`, `curl`, and `make`

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd llm-fast-api
```

````

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Setup

### 1. Install `llama.cpp` with Metal Support

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
LLAMA_METAL=1 make -j$(sysctl -n hw.logicalcpu)
cd ..
```

### 2. Download the Gemma 3 27B Instruct Model

```bash
mkdir -p models
curl -L -o models/google_gemma-3-27b-it-q4_K_M.gguf \
  https://huggingface.co/TheBloke/gemma-1.1-7B-Instruct-GGUF/resolve/main/google_gemma-3-27b-it-q4_K_M.gguf
```

> Replace the URL if you are hosting the 27B model elsewhere.

### 3. Run `llama-server` Locally (Metal GPU)

```bash
./llama.cpp/server/llama-server \
  -m models/google_gemma-3-27b-it-q4_K_M.gguf \
  --model-alias google_gemma-3-27b-it \
  --threads 32 \
  --gpu-layers 60 \
  -c 8192 \
  --mlock \
  --host 127.0.0.1 \
  --port 8080 \
  > llama-server.log 2>&1 &
```

> Optional: Monitor logs with `tail -f llama-server.log`

---

## 🐳 Start FastAPI Proxy Server (Docker)

```bash
docker compose up --build
```

---

## 🌐 API Endpoints

### ✅ OpenAI-Compatible Chat Completion

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

### 🔁 Direct llama.cpp Completion API

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

---

## 📂 Project Structure

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
├── llama.cpp/         # llama.cpp compiled with Metal support
├── models/            # Your GGUF model files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔐 Environment Configuration

Set via Docker or `.env` file (optional):

- `LLM_SERVER_URL=http://host.docker.internal:8080`

---

## ⚙️ Development

```bash
# Local hot-reload development
uvicorn app.main:app --reload

# Or inside Docker
docker compose build
docker compose up
```

---

## 🚦 Performance Tips

- Make sure you use the `--mlock` flag for best performance on macOS
- Metal GPU acceleration is enabled via `LLAMA_METAL=1`
- Keep logs open via: `tail -f llama-server.log`

---

## 📜 License

[Your License Here]

---

## 🤝 Contributing

[Your Contribution Guidelines Here]

---
````
