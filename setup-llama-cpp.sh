#!/bin/bash

set -e

# 🧠 Model setup
MODEL_NAME="google_gemma-3-27b-it-q4_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/gemma-1.1-7B-Instruct-GGUF/resolve/main/${MODEL_NAME}"  # Change this if you have the 27B hosted elsewhere
MODEL_DIR="./models"
MODEL_PATH="${MODEL_DIR}/${MODEL_NAME}"

# ⚙️ Llama server settings
THREADS=32
GPU_LAYERS=60
CONTEXT=8192
PORT=8080
HOST="0.0.0.0"
LOG_FILE="llama-server.log"

echo "🛠️ Building llama.cpp with Metal support..."

if [ ! -d llama.cpp ]; then
  git clone https://github.com/ggerganov/llama.cpp.git
  cd llama.cpp
  LLAMA_METAL=1 make -j$(sysctl -n hw.logicalcpu)
  cd ..
else
  echo "✅ llama.cpp already set up."
fi

# 📦 Download model
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_PATH" ]; then
  echo "⬇️ Downloading Gemma model..."
  curl -L "$MODEL_URL" -o "$MODEL_PATH"
else
  echo "✅ Model already exists."
fi

# 🔁 Kill any previous server
pkill -f "llama-server" || true

echo "🚀 Launching llama-server with GPU acceleration..."
./llama.cpp/server/llama-server \
  -m "$MODEL_PATH" \
  --model-alias "google_gemma-3-27b-it" \
  --threads $THREADS \
  --gpu-layers $GPU_LAYERS \
  -c $CONTEXT \
  --mlock \
  --port $PORT \
  --host $HOST \
  > "$LOG_FILE" 2>&1 &

sleep 3

echo "✅ Gemma 3 27B is live at http://${HOST}:${PORT}"
echo "📄 Logs: tail -f $LOG_FILE"
