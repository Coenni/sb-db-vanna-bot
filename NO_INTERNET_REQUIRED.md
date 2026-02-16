# Using Vanna AI Without Internet Connection

**Question:** "I want to use offline models without internet connection"

**Answer:** ✅ **YES! You can run this application completely offline!**

## Quick Setup (5 Steps)

### 1. Install Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

### 2. Download a Model (While You Have Internet)

```bash
# This is the ONLY time you need internet
ollama pull llama2
```

**That's it!** You can now disconnect from the internet.

### 3. Configure for Offline Mode

Edit `.env`:
```bash
cp .env.example .env
```

Set these values:
```env
LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

**No OpenAI API key needed!**

### 4. Start Ollama

```bash
ollama serve
```

Leave this running in a terminal.

### 5. Start the Application

```bash
docker compose up -d
```

## ✅ You're Now Running Completely Offline!

- ❌ No internet connection required
- ❌ No OpenAI API key required
- ❌ No API costs
- ✅ Complete privacy (data stays on your machine)
- ✅ Unlimited queries
- ✅ Free forever

## How It Works

Instead of sending your questions to OpenAI's servers over the internet, the application now uses **Ollama** - a tool that runs AI models locally on your computer.

**Before (OpenAI - requires internet):**
```
Your Question → Internet → OpenAI Servers → Response → Internet → You
💰 Costs money | ☁️ Cloud-based | 🌐 Requires internet
```

**Now (Ollama - offline):**
```
Your Question → Your Local Ollama → Response → You
💚 Free | 🔒 Private | 📡 No internet needed
```

## Test It

1. **Disconnect from the internet**
2. Open http://localhost:4200
3. Ask: "How many customers do we have?"
4. Get instant results - all processed locally!

## Switching Between Online/Offline

You can switch anytime by editing `.env`:

**Use Offline (Ollama):**
```env
LLM_PROVIDER=ollama
```

**Use Online (OpenAI):**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

Then restart:
```bash
docker compose restart vanna-service
```

## Need More Details?

See [OFFLINE_SETUP.md](OFFLINE_SETUP.md) for:
- Detailed setup instructions
- Different model options
- Docker containerized Ollama
- Performance optimization
- Troubleshooting
- Hardware requirements

## Summary

**What you asked for:** "Use offline models without internet connection"

**What you got:**
- ✅ Offline operation via Ollama
- ✅ No internet required (after initial setup)
- ✅ No API key required
- ✅ No costs
- ✅ Complete privacy
- ✅ Easy setup (5 steps)
- ✅ Same features as online mode

**All your prerequisites are now optional!**
- ~~OpenAI API key~~ → **Not needed for offline mode**
- ~~Internet connection~~ → **Not needed for offline mode**

Enjoy your completely offline, private, and free Vanna AI experience! 🎉
