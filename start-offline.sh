#!/bin/bash

# Offline Startup Script for Vanna AI
# This script starts the application in offline mode using Ollama

set -e

echo "=========================================="
echo "  Vanna AI - Offline Mode Startup"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Check if docker-compose.offline.yml exists
if [ ! -f "docker-compose.offline.yml" ]; then
    echo "❌ Error: docker-compose.offline.yml not found"
    echo "Please run this script from the repository root directory"
    exit 1
fi

echo "Starting services in offline mode..."
echo ""
echo "📦 This will:"
echo "  1. Start PostgreSQL with sample data"
echo "  2. Start Ollama (local LLM server)"
echo "  3. Download llama2 model (~4GB, first time only)"
echo "  4. Start Vanna AI service (configured for Ollama)"
echo "  5. Start Backend and Frontend"
echo ""
echo "⏱️  First run will take 5-10 minutes to download the model"
echo "   Subsequent runs will be much faster (~1 minute)"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

echo ""
echo "Starting services..."
echo ""

# Start with docker-compose offline configuration
docker compose -f docker-compose.yml -f docker-compose.offline.yml up -d

echo ""
echo "=========================================="
echo "  Services Starting..."
echo "=========================================="
echo ""
echo "Checking service status..."
sleep 5

# Show status
docker compose -f docker-compose.yml -f docker-compose.offline.yml ps

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "🎉 Application is running in OFFLINE mode"
echo ""
echo "📊 Access the application:"
echo "   Frontend: http://localhost:4200"
echo "   Backend:  http://localhost:8080"
echo ""
echo "🔍 Check logs:"
echo "   All services: docker compose -f docker-compose.yml -f docker-compose.offline.yml logs -f"
echo "   Ollama only:  docker compose -f docker-compose.yml -f docker-compose.offline.yml logs -f ollama"
echo "   Vanna only:   docker compose -f docker-compose.yml -f docker-compose.offline.yml logs -f vanna-service"
echo ""
echo "🛑 Stop services:"
echo "   docker compose -f docker-compose.yml -f docker-compose.offline.yml down"
echo ""
echo "✅ No internet connection required from this point!"
echo "   All processing happens locally on your machine."
echo ""
