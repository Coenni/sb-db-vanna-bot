"""
Vanna Ollama Integration for Offline LLM Support

This module provides integration with Ollama to use local LLM models
without requiring internet connection or API keys.

Ollama must be running locally at the configured endpoint.
"""

import requests
import logging
from typing import List

logger = logging.getLogger(__name__)


class Ollama_Chat:
    """
    Vanna integration with Ollama for offline LLM inference.
    
    This class provides the necessary methods for Vanna to use Ollama
    as the LLM backend instead of OpenAI or other cloud-based services.
    """
    
    def __init__(self, config=None):
        """
        Initialize Ollama chat integration.
        
        Args:
            config: Dictionary with configuration options:
                - ollama_host: Ollama API endpoint (default: http://localhost:11434)
                - model: Model name to use (default: llama2)
        """
        if config is None:
            config = {}
        
        self.ollama_host = config.get('ollama_host', 'http://localhost:11434')
        self.model = config.get('model', 'llama2')
        
        logger.info(f"Initialized Ollama chat with model: {self.model} at {self.ollama_host}")
        
        # Verify Ollama is accessible
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                logger.info(f"Available Ollama models: {model_names}")
                
                # Check if requested model is available
                if self.model not in model_names:
                    logger.warning(f"Model '{self.model}' not found in available models. "
                                 f"Available: {model_names}. Model will be pulled on first use.")
            else:
                logger.warning(f"Could not connect to Ollama at {self.ollama_host}")
        except Exception as e:
            logger.warning(f"Could not verify Ollama connection: {str(e)}")
            logger.info("Ollama must be running for the application to work. "
                       "Install: https://ollama.ai")
    
    def system_message(self, message: str) -> dict:
        """
        Create a system message for the LLM.
        
        Args:
            message: The system message content
            
        Returns:
            dict: Message in Ollama format
        """
        return {"role": "system", "content": message}
    
    def user_message(self, message: str) -> dict:
        """
        Create a user message for the LLM.
        
        Args:
            message: The user message content
            
        Returns:
            dict: Message in Ollama format
        """
        return {"role": "user", "content": message}
    
    def assistant_message(self, message: str) -> dict:
        """
        Create an assistant message for the LLM.
        
        Args:
            message: The assistant message content
            
        Returns:
            dict: Message in Ollama format
        """
        return {"role": "assistant", "content": message}
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        """
        Submit a prompt to Ollama and get a response.
        
        This is the main method Vanna uses to interact with the LLM.
        
        Args:
            prompt: List of message dictionaries or a string prompt
            **kwargs: Additional parameters (e.g., temperature, max_tokens)
            
        Returns:
            str: The LLM's response
        """
        try:
            # Handle both message list and string formats
            if isinstance(prompt, list):
                messages = prompt
            else:
                messages = [self.user_message(str(prompt))]
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get('temperature', 0.7),
                }
            }
            
            # Add max_tokens if provided
            if 'max_tokens' in kwargs:
                payload['options']['num_predict'] = kwargs['max_tokens']
            
            logger.info(f"Submitting prompt to Ollama model: {self.model}")
            
            # Make request to Ollama
            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json=payload,
                timeout=120  # Longer timeout for local inference
            )
            
            response.raise_for_status()
            
            # Extract the response content
            result = response.json()
            content = result.get('message', {}).get('content', '')
            
            logger.info(f"Received response from Ollama ({len(content)} chars)")
            
            return content
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error communicating with Ollama: {str(e)}"
            logger.error(error_msg)
            logger.error("Make sure Ollama is running: ollama serve")
            logger.error(f"And the model is available: ollama pull {self.model}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error in Ollama prompt submission: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def generate_sql(self, question: str, **kwargs) -> str:
        """
        Generate SQL from a natural language question.
        
        This method is called by Vanna to generate SQL queries.
        
        Args:
            question: Natural language question
            **kwargs: Additional parameters
            
        Returns:
            str: Generated SQL query
        """
        # This method will be overridden by Vanna's base implementation
        # which uses submit_prompt internally
        pass
