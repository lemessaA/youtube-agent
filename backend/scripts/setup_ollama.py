#!/usr/bin/env python3
"""
Ollama setup script for YouTube Automation System
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Ollama is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    logger.error("Ollama is not installed")
    return False

def install_ollama():
    """Install Ollama"""
    logger.info("Installing Ollama...")
    
    try:
        # Install Ollama
        subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh', '|', 'sh'], check=True)
        logger.info("Ollama installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Ollama: {e}")
        return False

def start_ollama():
    """Start Ollama service"""
    logger.info("Starting Ollama service...")
    
    try:
        # Try to start Ollama
        subprocess.run(['ollama', 'serve'], check=True, timeout=5)
        return True
    except subprocess.TimeoutExpired:
        # Service started but command didn't return (expected)
        logger.info("Ollama service started")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start Ollama: {e}")
        return False
    except FileNotFoundError:
        logger.error("Ollama command not found")
        return False

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            logger.info("Ollama is running")
            return True
    except requests.exceptions.RequestException:
        pass
    
    logger.error("Ollama is not running")
    return False

def list_available_models():
    """List available models"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                logger.info("Available models:")
                for model in models:
                    logger.info(f"  - {model['name']}")
                return [model['name'] for model in models]
            else:
                logger.info("No models installed")
                return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to list models: {e}")
        return []

def pull_model(model_name):
    """Pull a model"""
    logger.info(f"Pulling model: {model_name}")
    
    try:
        response = requests.post(
            'http://localhost:11434/api/pull',
            json={'name': model_name},
            timeout=600  # 10 minutes timeout
        )
        
        if response.status_code == 200:
            logger.info(f"Model {model_name} pulled successfully")
            return True
        else:
            logger.error(f"Failed to pull model {model_name}: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to pull model {model_name}: {e}")
        return False

def setup_recommended_models():
    """Setup recommended models for YouTube automation"""
    recommended_models = [
        'llama3.1:8b',      # Good for general tasks
        'qwen2.5:7b',       # Good for structured data
        'codellama:7b',      # Good for technical content
    ]
    
    available_models = list_available_models()
    
    for model in recommended_models:
        if model not in available_models:
            logger.info(f"Installing recommended model: {model}")
            if not pull_model(model):
                logger.error(f"Failed to install {model}")
        else:
            logger.info(f"Model {model} already available")

def update_env_file():
    """Update .env file with Ollama configuration"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    # Create .env from example if it doesn't exist
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        logger.info("Created .env file from .env.example")
    
    # Update .env with Ollama settings
    if env_file.exists():
        content = env_file.read_text()
        
        # Add Ollama settings if not present
        if 'OLLAMA_BASE_URL' not in content:
            content += '\n# Ollama Local Models\n'
            content += 'OLLAMA_BASE_URL=http://localhost:11434\n'
            content += 'OLLAMA_MODEL=llama3.1:8b\n'
            content += 'OLLAMA_TEMPERATURE=0.7\n'
            
            env_file.write_text(content)
            logger.info("Added Ollama configuration to .env file")

def main():
    """Main setup function"""
    logger.info("YouTube Automation System - Ollama Setup")
    logger.info("=" * 50)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        logger.info("Installing Ollama...")
        if not install_ollama():
            logger.error("Failed to install Ollama")
            sys.exit(1)
    
    # Check if Ollama is running
    if not check_ollama_running():
        logger.info("Starting Ollama service...")
        if not start_ollama():
            logger.error("Failed to start Ollama")
            logger.info("Please start Ollama manually with: ollama serve")
            sys.exit(1)
        
        # Wait a bit for service to start
        import time
        time.sleep(3)
        
        if not check_ollama_running():
            logger.error("Ollama is still not running")
            sys.exit(1)
    
    # Setup models
    logger.info("Setting up recommended models...")
    setup_recommended_models()
    
    # Update environment file
    update_env_file()
    
    # List final status
    logger.info("\n" + "=" * 50)
    logger.info("Setup completed!")
    logger.info("Available models:")
    models = list_available_models()
    if models:
        for model in models:
            logger.info(f"  - {model}")
    else:
        logger.info("  No models found")
    
    logger.info("\nNext steps:")
    logger.info("1. Update your .env file with your preferred model")
    logger.info("2. Run: python scripts/test_system.py")
    logger.info("3. Start the application: python -m app.main")

if __name__ == "__main__":
    main()
