# OFFLINE MODE - Quick Reference

## One Command Setup

**Linux/Mac:**
```bash
./start-offline.sh
```

**Windows:**
```bash
start-offline.bat
```

**Manual:**
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml up -d
```

## What It Does

1. ✅ Starts PostgreSQL with sample data
2. ✅ Starts Ollama container (local LLM server)
3. ✅ Downloads llama2 model automatically (~4GB, first time only)
4. ✅ Configures Vanna to use Ollama
5. ✅ Starts backend and frontend
6. ✅ **Works completely offline after first run!**

## First Run vs Subsequent Runs

| Aspect | First Run | Subsequent Runs |
|--------|-----------|-----------------|
| Internet needed | ✅ Yes (to download model) | ❌ No |
| Time | 5-10 minutes | ~1 minute |
| Downloads | Ollama image + llama2 model (~5GB total) | Nothing |

## Access the Application

- **Frontend:** http://localhost:4200
- **Backend:** http://localhost:8080
- **Ollama:** http://localhost:11434

## Common Commands

**Start offline mode:**
```bash
./start-offline.sh
```

**View logs:**
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml logs -f
```

**Stop services:**
```bash
docker compose -f docker-compose.yml -f docker-compose.offline.yml down
```

**Check if Ollama is ready:**
```bash
curl http://localhost:11434/api/tags
```

**List downloaded models:**
```bash
docker exec ollama ollama list
```

## Verify Offline Operation

1. Start services with `./start-offline.sh`
2. Wait for setup to complete
3. **Disconnect from internet**
4. Open http://localhost:4200
5. Ask a question: "How many customers do we have?"
6. If you get a response, you're running completely offline! ✅

## What's Different from Online Mode

| Feature | Online (OpenAI) | Offline (Ollama) |
|---------|----------------|------------------|
| Internet | Required | Not required |
| API Key | Required | Not required |
| Cost | $0.002 per 1K tokens | Free |
| Privacy | Data sent to cloud | Data stays local |
| Speed | Fast | Medium |
| Quality | Excellent | Good |
| Setup | Simple (.env file) | One script |

## Files Involved

- `docker-compose.yml` - Base configuration
- `docker-compose.offline.yml` - Offline mode overrides
- `start-offline.sh` - Linux/Mac startup script
- `start-offline.bat` - Windows startup script
- `NO_INTERNET_REQUIRED.md` - Full guide
- `OFFLINE_SETUP.md` - Detailed setup instructions

## Troubleshooting

**Problem: "Cannot connect to Ollama"**
- Solution: Wait for model download to complete
- Check: `docker compose -f docker-compose.yml -f docker-compose.offline.yml logs ollama`

**Problem: "Model download takes too long"**
- Solution: Be patient, llama2 is ~4GB
- Alternative: Use smaller model (edit docker-compose.offline.yml)

**Problem: "Out of disk space"**
- Solution: Free up at least 10GB disk space
- Models are stored in `ollama-data` Docker volume

## Switch Back to Online Mode

```bash
# Stop offline mode
docker compose -f docker-compose.yml -f docker-compose.offline.yml down

# Edit .env
echo "LLM_PROVIDER=openai" >> .env
echo "OPENAI_API_KEY=your-key" >> .env

# Start normal mode
docker compose up -d
```

## Summary

**To run completely offline:**
1. Run `./start-offline.sh` (one time setup)
2. Wait for model download (first time only)
3. Disconnect from internet
4. Use application normally

**No manual Ollama installation needed!**
**No configuration files to edit!**
**Just one script!**
