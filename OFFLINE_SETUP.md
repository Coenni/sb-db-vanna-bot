# Offline Setup Guide - Using Vanna AI Without Internet

This guide explains how to run the Vanna AI application completely offline using local LLM models via Ollama, without requiring an internet connection or OpenAI API key.

## Overview

The application supports two LLM providers:

| Provider | Requires Internet | Requires API Key | Cost | Privacy |
|----------|-------------------|------------------|------|---------|
| **OpenAI** (default) | ✅ Yes | ✅ Yes | 💰 Pay per use | ☁️ Cloud-based |
| **Ollama** (offline) | ❌ No | ❌ No | 💚 Free | 🔒 Fully local |

## Quick Start - Offline Mode

### Prerequisites

1. **Docker and Docker Compose** installed
2. **Ollama** installed ([https://ollama.ai](https://ollama.ai))
3. **No internet required** after initial setup!

### Step 1: Install Ollama

**On Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**On Windows:**
Download from [https://ollama.ai/download](https://ollama.ai/download)

**Verify installation:**
```bash
ollama --version
```

### Step 2: Pull a Model

Download a model while you have internet (one-time):

```bash
# Recommended for SQL generation (balanced size/performance)
ollama pull llama2

# Alternative options:
ollama pull mistral        # Faster, smaller
ollama pull codellama      # Better for code/SQL
ollama pull llama3         # Latest, better quality
ollama pull mixtral        # High quality, larger
```

**Check available models:**
```bash
ollama list
```

### Step 3: Configure for Offline Mode

**Edit `.env` file:**
```bash
cp .env.example .env
```

Set the LLM provider to Ollama:
```env
# Choose Ollama for offline mode
LLM_PROVIDER=ollama

# Ollama configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# No OpenAI key required!
# OPENAI_API_KEY=not-needed-for-ollama
```

### Step 4: Start Ollama (if not already running)

```bash
ollama serve
```

Leave this running in a terminal window.

### Step 5: Start the Application

```bash
docker compose up -d
```

**That's it!** The application now runs completely offline.

## Using Ollama in Docker (Fully Containerized)

If you want everything in Docker containers:

### Step 1: Edit docker-compose.yml

Uncomment the Ollama service:

```yaml
services:
  # Ollama Service (Optional - for offline LLM)
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    networks:
      - vanna-network

  vanna-service:
    # ...
    environment:
      LLM_PROVIDER: ollama
      OLLAMA_HOST: http://ollama:11434  # Use container name
      OLLAMA_MODEL: llama2
    depends_on:
      - postgres
      - ollama  # Add dependency

volumes:
  ollama-data:  # Add volume
```

### Step 2: Pull Model in Docker

Start Ollama container:
```bash
docker compose up -d ollama
```

Pull a model:
```bash
docker exec -it ollama ollama pull llama2
```

### Step 3: Start All Services

```bash
docker compose up -d
```

## Configuration Options

### Environment Variables

**In `.env` file:**

```bash
# ============================================================================
# LLM Provider Selection
# ============================================================================

# Choose: 'openai' or 'ollama'
LLM_PROVIDER=ollama

# ============================================================================
# Ollama Configuration (when LLM_PROVIDER=ollama)
# ============================================================================

# Ollama API endpoint
OLLAMA_HOST=http://localhost:11434

# Model to use
OLLAMA_MODEL=llama2
```

### Recommended Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama2** | 3.8GB | Fast | Good | General use, recommended |
| **mistral** | 4.1GB | Very Fast | Good | Quick responses |
| **codellama** | 3.8GB | Fast | Better for code | SQL generation |
| **llama3** | 4.7GB | Medium | Excellent | Best quality |
| **mixtral** | 26GB | Slow | Excellent | Maximum quality |

### Switch Between Providers

You can switch between OpenAI and Ollama at any time:

**Switch to Ollama:**
```bash
# Edit .env
LLM_PROVIDER=ollama

# Restart service
docker compose restart vanna-service
```

**Switch to OpenAI:**
```bash
# Edit .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# Restart service
docker compose restart vanna-service
```

## Verification

### Check Ollama is Running

```bash
curl http://localhost:11434/api/tags
```

Should return list of available models.

### Check Vanna Service

```bash
docker compose logs vanna-service | grep -i ollama
```

Should see:
```
Using Ollama for offline LLM
Initialized Ollama chat with model: llama2 at http://localhost:11434
```

### Test a Question

1. Open http://localhost:4200
2. Go to "Ask" page
3. Type: "How many customers do we have?"
4. Click "Ask"

The query should be processed using your local Ollama model!

## Troubleshooting

### "Could not connect to Ollama"

**Problem:** Vanna can't reach Ollama

**Solutions:**
1. Check Ollama is running: `ollama serve`
2. Verify endpoint: `curl http://localhost:11434/api/tags`
3. Check `OLLAMA_HOST` in `.env` matches your setup
4. If using Docker, use container name: `http://ollama:11434`

### "Model not found"

**Problem:** Requested model isn't pulled

**Solution:**
```bash
# Check available models
ollama list

# Pull the model you want
ollama pull llama2
```

### Slow Response Times

**Problem:** Queries take a long time

**Solutions:**
1. Use a smaller/faster model: `mistral` or `llama2`
2. Ensure Ollama has enough RAM (8GB+ recommended)
3. Use GPU acceleration if available
4. Consider using a more powerful machine

### Out of Memory

**Problem:** Ollama crashes or system freezes

**Solutions:**
1. Use smaller model: `mistral` instead of `mixtral`
2. Close other applications
3. Increase Docker memory limits
4. Use a machine with more RAM

## Performance Comparison

### OpenAI (Cloud)
- **Pros:** Fast, high quality, no local resources
- **Cons:** Requires internet, costs money, data sent to cloud

### Ollama (Local)
- **Pros:** Free, private, offline, no API limits
- **Cons:** Slower, requires good hardware, lower quality than GPT-4

### Hardware Requirements

**Minimum:**
- 8GB RAM
- 10GB disk space
- Modern CPU

**Recommended:**
- 16GB+ RAM
- 20GB+ disk space
- GPU (NVIDIA/AMD) for faster inference
- SSD for better performance

**Optimal:**
- 32GB+ RAM
- 50GB+ disk space
- Modern GPU (8GB+ VRAM)

## Advanced: GPU Acceleration

### NVIDIA GPU (Linux)

Install NVIDIA Container Toolkit:
```bash
# Add repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# Install toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Restart Docker
sudo systemctl restart docker
```

Update docker-compose.yml:
```yaml
ollama:
  image: ollama/ollama:latest
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

### Apple Silicon (M1/M2/M3)

Ollama automatically uses Metal for acceleration on Apple Silicon - no configuration needed!

## Offline Workflow

Once set up, the complete offline workflow:

```bash
# 1. Start Ollama (one time per boot)
ollama serve

# 2. Start application
docker compose up -d

# 3. Use application at http://localhost:4200
# - No internet needed
# - No API costs
# - Complete privacy

# 4. Stop application
docker compose down
```

## Network Requirements

### Initial Setup (one-time, requires internet)
- Install Docker
- Install Ollama
- Pull Docker images: `docker compose pull`
- Pull Ollama models: `ollama pull llama2`

### Runtime (NO internet required)
- ✅ Run application
- ✅ Ask questions
- ✅ Generate SQL
- ✅ Train model
- ✅ Use all features

## Benefits of Offline Mode

1. **🔒 Privacy:** Your data never leaves your machine
2. **💰 Cost:** No API fees, completely free
3. **🚀 No Rate Limits:** Unlimited queries
4. **📡 Offline:** Works without internet
5. **🔧 Customizable:** Use any Ollama-compatible model
6. **🎯 Reproducible:** Same model = same results

## Limitations

1. **Performance:** Slower than cloud APIs
2. **Quality:** May be lower than GPT-4
3. **Resources:** Requires good hardware
4. **Setup:** Initial setup more complex

## Summary

**For Offline Use:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Configure
echo "LLM_PROVIDER=ollama" >> .env

# Run
ollama serve &
docker compose up -d
```

**You're now running Vanna AI completely offline!** 🎉

No internet. No API keys. No costs. Complete privacy.

## Support

If you encounter issues:
1. Check Ollama logs: `docker logs ollama`
2. Check Vanna logs: `docker compose logs vanna-service`
3. Verify model is pulled: `ollama list`
4. Test Ollama directly: `ollama run llama2 "Hello"`

## Additional Resources

- Ollama Documentation: https://github.com/ollama/ollama
- Ollama Models: https://ollama.ai/library
- Vanna AI: https://github.com/vanna-ai/vanna
- Docker Documentation: https://docs.docker.com
