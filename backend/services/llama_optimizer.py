"""
Free Llama Model Support for Applytune

This module enables 100% FREE resume optimization using Meta's Llama models.
No API costs, no usage limits, complete privacy!

Options:
1. Ollama (RECOMMENDED): Run locally, 100% free, private
2. Groq: Free tier, super fast inference
3. Together AI: Free tier available
"""

import os
import json
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LlamaOptimizer:
    """
    Free resume optimization using Llama 3.1 models.
    
    Llama 3.1 70B is comparable to GPT-4 in quality but completely FREE!
    
    Providers:
    - Ollama: Run locally (100% free, private, no limits)
    - Groq: Cloud-hosted (free tier, super fast)
    - Together AI: Cloud-hosted (free tier + cheap paid)
    """
    
    def __init__(self):
        # Try providers in order: Ollama (best) -> Groq (fast) -> fail
        self.provider = os.getenv('LLAMA_PROVIDER', 'auto')  # auto, ollama, groq
        
        # Ollama settings (local, 100% FREE)
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1:70b')
        
        # Groq settings (cloud, FREE tier)
        self.groq_api_key = os.getenv('GROQ_API_KEY', '')
        # Updated to latest Groq model (Jan 2026)
        self.groq_model = 'llama-3.3-70b-versatile'  # NEW: Llama 3.3 (faster & better!)
        
        # Multiple model support via Ollama
        self.available_models = [
            'llama3.1:70b',      # Best quality
            'llama3.1:8b',       # Faster, less RAM
            'llama3.2:latest',   # Latest Llama
            'gemma2:9b',         # Google Gemma (also free)
            'mistral:latest',    # Mistral (free)
            'qwen2.5:14b',       # Qwen (free, multilingual)
        ]
        
        # Auto-detect best available provider
        if self.provider == 'auto':
            self.provider = self._auto_detect_provider()
        
        print(f"🦙 Llama provider: {self.provider}")
        
        # Check availability and show status
        if self.provider == 'ollama':
            self._check_ollama_available()
        elif self.provider == 'groq':
            if self.groq_api_key:
                print("✓ Groq API key found (FREE tier)")
            else:
                print("⚠️  No Groq API key. Using Ollama...")
                self.provider = 'ollama'
                self._check_ollama_available()
    
    def _auto_detect_provider(self) -> str:
        """
        Auto-detect the best available FREE provider.
        Priority: Ollama (best) -> Groq (fast) -> fail with helpful message
        """
        # Try Ollama first (100% free, private)
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                return 'ollama'
        except:
            pass
        
        # Try Groq (free tier, cloud)
        if self.groq_api_key:
            return 'groq'
        
        # No provider available - default to ollama with warning
        print("\n" + "="*60)
        print("⚠️  NO FREE AI PROVIDER FOUND!")
        print("="*60)
        print("\nTo use Applytune for FREE, choose one:")
        print("\n1. OLLAMA (RECOMMENDED - 100% Free, Private):")
        print("   brew install ollama")
        print("   ollama pull llama3.1:70b")
        print("\n2. GROQ (Free Tier - Fast, Cloud):")
        print("   Get free key: https://console.groq.com")
        print("   Add to .env: GROQ_API_KEY=gsk_...")
        print("\n" + "="*60 + "\n")
        
        return 'ollama'  # Default even if not available, will show error later
    
    def _check_ollama_available(self):
        """Check if Ollama is running and show helpful info"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                print(f"✓ Ollama available with {len(models)} models")
                
                # Check if our preferred model is available
                if self.ollama_model in model_names:
                    print(f"✓ Using model: {self.ollama_model}")
                else:
                    print(f"⚠️  Preferred model '{self.ollama_model}' not found")
                    
                    # Try to find an alternative
                    for alt_model in self.available_models:
                        if alt_model in model_names:
                            print(f"✓ Found alternative: {alt_model}")
                            self.ollama_model = alt_model
                            break
                    else:
                        print(f"\n💡 Download models:")
                        print(f"   ollama pull llama3.1:70b   (Best quality)")
                        print(f"   ollama pull llama3.1:8b    (Faster)")
                
                return True
            else:
                print("⚠️  Ollama not responding")
                return False
        except Exception as e:
            print(f"\n⚠️  Ollama not running!")
            print(f"   Error: {e}")
            print("\n💡 Quick setup:")
            print("   1. Install: brew install ollama")
            print("   2. Download model: ollama pull llama3.1:70b")
            print("   3. It auto-starts, or run: ollama serve")
            print("\n   Or use Groq (free): https://console.groq.com")
            return False
    
    def optimize_text(self, prompt: str, system_prompt: str, 
                     temperature: float = 0.5,
                     max_tokens: int = 500) -> str:
        """
        Optimize text using Llama model.
        
        This works the same as OpenAI/Claude but is 100% FREE!
        """
        if self.provider == 'ollama':
            return self._optimize_with_ollama(prompt, system_prompt, temperature, max_tokens)
        elif self.provider == 'groq':
            return self._optimize_with_groq(prompt, system_prompt, temperature, max_tokens)
        elif self.provider == 'together':
            return self._optimize_with_together(prompt, system_prompt, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _optimize_with_ollama(self, prompt: str, system_prompt: str,
                              temperature: float, max_tokens: int) -> str:
        """
        Use Ollama for local Llama inference.
        
        Benefits:
        - 100% FREE
        - No API keys needed
        - Complete privacy (runs on your machine)
        - No rate limits
        - No usage tracking
        
        Requirements:
        - Install Ollama: https://ollama.ai
        - Run: ollama pull llama3.1:70b
        """
        try:
            # Prepare request
            url = f"{self.ollama_url}/api/generate"
            
            # Combine system and user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            payload = {
                "model": self.ollama_model,
                "prompt": full_prompt,
                "temperature": temperature,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '').strip()
        
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Ollama not running. Start it with: ollama serve\n"
                "Or install from: https://ollama.ai"
            )
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
    
    def _optimize_with_groq(self, prompt: str, system_prompt: str,
                           temperature: float, max_tokens: int) -> str:
        """
        Use Groq for super-fast Llama inference.
        
        Benefits:
        - FREE tier available
        - Extremely fast (fastest Llama inference)
        - No local setup needed
        
        Get free API key: https://console.groq.com
        """
        if not self.groq_api_key:
            raise ValueError(
                "Groq API key not set. Get free key from: https://console.groq.com\n"
                "Add to .env: GROQ_API_KEY=your_key"
            )
        
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.groq_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def _optimize_with_together(self, prompt: str, system_prompt: str,
                                temperature: float, max_tokens: int) -> str:
        """
        Use Together AI for hosted Llama models.
        
        Benefits:
        - FREE tier available ($25 credit)
        - Good performance
        - Multiple model options
        
        Get free API key: https://api.together.xyz
        """
        if not self.together_api_key:
            raise ValueError(
                "Together API key not set. Get free key from: https://api.together.xyz\n"
                "Add to .env: TOGETHER_API_KEY=your_key"
            )
        
        try:
            url = "https://api.together.xyz/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.together_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.together_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        
        except Exception as e:
            raise Exception(f"Together AI error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if the selected provider is available"""
        if self.provider == 'ollama':
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
                return response.status_code == 200
            except:
                return False
        elif self.provider == 'groq':
            return bool(self.groq_api_key)
        elif self.provider == 'together':
            return bool(self.together_api_key)
        return False
    
    def get_cost_estimate(self) -> str:
        """Get cost estimate for this provider"""
        costs = {
            'ollama': '$0.00 - Runs locally (electricity only!)',
            'groq': '$0.00 - Free tier (rate limited)',
            'together': '$0.00 - $25 free credit, then ~$0.001/resume'
        }
        return costs.get(self.provider, 'Unknown')


# Convenience function for easy integration
def optimize_with_llama(prompt: str, system_prompt: str,
                       temperature: float = 0.5,
                       max_tokens: int = 500) -> str:
    """
    Simple function to optimize text with Llama.
    Automatically uses the best available provider.
    """
    optimizer = LlamaOptimizer()
    
    if not optimizer.is_available():
        # Provide helpful error message
        if optimizer.provider == 'ollama':
            raise Exception(
                "Ollama not available. To use FREE Llama models:\n"
                "1. Install Ollama: https://ollama.ai\n"
                "2. Run: ollama pull llama3.1:70b\n"
                "3. Start: ollama serve"
            )
        elif optimizer.provider == 'groq':
            raise Exception(
                "Groq API key not set. Get free key from: https://console.groq.com"
            )
        elif optimizer.provider == 'together':
            raise Exception(
                "Together API key not set. Get free key from: https://api.together.xyz"
            )
    
    return optimizer.optimize_text(prompt, system_prompt, temperature, max_tokens)
