#!/bin/bash
# Setup script for Ollama (fully private AI)

set -e

echo "🔒 Setting up Ollama for fully private AI (data never leaves your network)..."
echo ""

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is already installed"
    ollama --version
else
    echo "📥 Installing Ollama..."
    echo "   This will download and install Ollama on your system"
    curl -fsSL https://ollama.ai/install.sh | sh
    
    if [ $? -eq 0 ]; then
        echo "✓ Ollama installed successfully"
    else
        echo "❌ Failed to install Ollama"
        echo "   Please install manually from https://ollama.ai"
        exit 1
    fi
fi

echo ""
echo "📦 Downloading required models..."
echo "   This may take several minutes depending on your internet connection"
echo ""

# Pull LLM model
echo "1. Downloading LLM model (llama3.2)..."
ollama pull llama3.2

# Pull embedding model
echo ""
echo "2. Downloading embedding model (nomic-embed-text)..."
ollama pull nomic-embed-text

echo ""
echo "✅ Ollama setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Make sure Ollama is running: ollama serve"
echo "   2. Update your .env file with:"
echo "      LLM_PROVIDER=ollama"
echo "      EMBEDDING_PROVIDER=ollama"
echo "   3. Start the application: uvicorn app.main:app --reload"
echo ""
echo "💡 Tip: Keep 'ollama serve' running in a separate terminal"
echo "   or run it in the background: ollama serve &"
echo ""

