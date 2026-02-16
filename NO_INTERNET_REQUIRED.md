# Using Vanna AI Without Internet Connection

**Question:** "Now when I run docker-compose up local without internet, language model will be active?"

**Answer:** ✅ **YES! Use the offline startup script!**

## Super Simple Setup (2 Steps!)

### Option 1: Use the Startup Script (Recommended)

**Linux/Mac:**
```bash
./start-offline.sh
```

**Windows:**
```batch
start-offline.bat
```

**That's it!** The script will:
- ✅ Start all services with Ollama
- ✅ Download llama2 model automatically (first time only)
- ✅ Configure everything for offline use
- ✅ No manual configuration needed!

### Option 2: Manual Docker Compose

```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml up -d
```

This uses the offline configuration that:
- Includes Ollama service
- Auto-downloads llama2 model
- Configures Vanna to use Ollama
- Works completely offline

## What Happens on First Run

1. **First Time (Requires Internet - One Time Only)**
   - Downloads Ollama Docker image (~1GB)
   - Downloads llama2 model (~4GB)
   - Takes 5-10 minutes depending on your connection

2. **After First Run (NO Internet Needed)**
   - Starts in ~1 minute
   - Everything runs offline
   - Model is cached locally

## ✅ You're Now Running Completely Offline!

After the first run:
- ❌ No internet connection required
- ❌ No OpenAI API key required
- ❌ No API costs
- ✅ Complete privacy (data stays on your machine)
- ✅ Unlimited queries
- ✅ Free forever

## Test It Works Offline

1. Run the startup script (first time)
2. Wait for setup to complete
3. **Disconnect from the internet**
4. Open http://localhost:4200
5. Ask: "How many customers do we have?"
6. Get instant results - all processed locally!

## Comparison

### Before (Manual Setup)

```bash
# Install Ollama separately
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model manually  
ollama pull llama2

# Start Ollama separately
ollama serve &

# Configure .env manually
echo "LLM_PROVIDER=ollama" > .env

# Start application
docker compose up -d
```

### Now (Automatic Setup)

```bash
# One command does everything!
./start-offline.sh
```

## Advanced: If You Already Have Ollama Installed

If you already have Ollama installed on your machine (not in Docker):

**Edit `.env`:**
```env
LLM_PROVIDER=ollama
OLLAMA_HOST=http://host.docker.internal:11434  # For Mac/Windows
# Or
OLLAMA_HOST=http://172.17.0.1:11434  # For Linux
```

**Then use regular docker-compose:**
```bash
docker compose up -d
```

## Managing the Offline Setup

**View logs:**
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml logs -f
```

**Stop services:**
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml down
```

**Restart services:**
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml restart
```

**Check model status:**
```bash
docker exec ollama ollama list
```

## Switch to Different Model

You can use different models by editing `docker-compose.offline.yml`:

```yaml
vanna-service:
  environment:
    OLLAMA_MODEL: mistral  # or codellama, llama3, etc.
```

Then rebuild:
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml up -d
```

## Troubleshooting

### "Model download failed"

Make sure you have internet on first run. The llama2 model is ~4GB.

### "Ollama service unhealthy"

Check logs:
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml logs ollama
```

### Services start but can't connect to Ollama

Wait a bit longer - model download can take time on first run. Check progress:
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml logs -f ollama
```

## Summary

**Your Question:** "Now when I run docker-compose up local without internet, language model will be active?"

**Answer:** 

✅ **YES!** Just use:
```bash
./start-offline.sh
```

**After first run, you can:**
- ✅ Disconnect from internet
- ✅ Use the application normally
- ✅ All LLM processing happens locally

**No manual Ollama installation needed!**
**No configuration needed!**
**Just run the script!**

The application now works completely offline with one simple command! 🎉
