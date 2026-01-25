"""
Multi-Model AI Optimizer - Support for multiple AI providers

This allows Applytune to work with different AI models for the best results.
Users can choose based on their needs: quality, speed, or cost.
"""

import os
from typing import Dict, Optional
from openai import OpenAI
import anthropic


class MultiModelOptimizer:
    """
    Supports multiple AI providers for resume optimization.
    
    Providers:
    - OpenAI (GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
    - Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
    - Google (Gemini 1.5 Pro) - Coming soon
    
    Each has different strengths:
    - GPT-4o: Best overall, fast, great at style preservation
    - Claude 3.5 Sonnet: Excellent at maintaining tone, longer context
    - GPT-4-turbo: Good balance of speed and quality
    """
    
    def __init__(self):
        # Initialize available clients
        self.openai_client = None
        self.anthropic_client = None
        
        # Try to initialize OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != 'your_openai_api_key_here':
            self.openai_client = OpenAI(api_key=openai_key)
            print("✓ OpenAI client initialized")
        
        # Try to initialize Anthropic (Claude)
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            print("✓ Anthropic (Claude) client initialized")
        
        # Get preferred model from environment
        self.default_model = os.getenv('AI_MODEL', 'gpt-4o')
        
        # Model capabilities and costs (per 1M tokens)
        self.models = {
            # OpenAI models
            'gpt-4o': {
                'provider': 'openai',
                'name': 'GPT-4o',
                'description': 'Latest OpenAI model, best quality and speed',
                'input_cost': 5.00,
                'output_cost': 15.00,
                'context_window': 128000,
                'best_for': 'Overall best choice - fast and accurate'
            },
            'gpt-4-turbo': {
                'provider': 'openai',
                'name': 'GPT-4 Turbo',
                'description': 'Fast GPT-4 variant, good balance',
                'input_cost': 10.00,
                'output_cost': 30.00,
                'context_window': 128000,
                'best_for': 'Good balance of speed and quality'
            },
            'gpt-4': {
                'provider': 'openai',
                'name': 'GPT-4',
                'description': 'Original GPT-4, very capable',
                'input_cost': 30.00,
                'output_cost': 60.00,
                'context_window': 8192,
                'best_for': 'High quality, but slower and more expensive'
            },
            'gpt-3.5-turbo': {
                'provider': 'openai',
                'name': 'GPT-3.5 Turbo',
                'description': 'Fast and cheap, decent quality',
                'input_cost': 0.50,
                'output_cost': 1.50,
                'context_window': 16385,
                'best_for': 'Budget option, good for simple optimizations'
            },
            
            # Anthropic models
            'claude-3-5-sonnet-20241022': {
                'provider': 'anthropic',
                'name': 'Claude 3.5 Sonnet',
                'description': 'Excellent at maintaining tone and style',
                'input_cost': 3.00,
                'output_cost': 15.00,
                'context_window': 200000,
                'best_for': 'Best for preserving writing style, huge context'
            },
            'claude-3-opus-20240229': {
                'provider': 'anthropic',
                'name': 'Claude 3 Opus',
                'description': 'Most capable Claude model',
                'input_cost': 15.00,
                'output_cost': 75.00,
                'context_window': 200000,
                'best_for': 'Highest quality from Anthropic'
            }
        }
    
    def get_available_models(self) -> Dict:
        """Return list of available models based on configured API keys"""
        available = {}
        
        for model_id, info in self.models.items():
            if info['provider'] == 'openai' and self.openai_client:
                available[model_id] = info
            elif info['provider'] == 'anthropic' and self.anthropic_client:
                available[model_id] = info
        
        return available
    
    def optimize_text(self, prompt: str, system_prompt: str, 
                     model: Optional[str] = None,
                     temperature: float = 0.5,
                     max_tokens: int = 500) -> str:
        """
        Optimize text using specified model or default.
        
        This abstracts away the differences between providers
        so the rest of the code doesn't need to worry about it.
        """
        model = model or self.default_model
        
        if model not in self.models:
            raise ValueError(f"Unknown model: {model}")
        
        model_info = self.models[model]
        provider = model_info['provider']
        
        if provider == 'openai':
            return self._optimize_with_openai(prompt, system_prompt, model, temperature, max_tokens)
        elif provider == 'anthropic':
            return self._optimize_with_claude(prompt, system_prompt, model, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _optimize_with_openai(self, prompt: str, system_prompt: str,
                              model: str, temperature: float, max_tokens: int) -> str:
        """Use OpenAI models (GPT-4o, GPT-4, etc.)"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Set OPENAI_API_KEY.")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _optimize_with_claude(self, prompt: str, system_prompt: str,
                             model: str, temperature: float, max_tokens: int) -> str:
        """
        Use Anthropic Claude models.
        
        Claude is excellent at maintaining writing style and has a huge
        context window (200K tokens) which is great for long resumes.
        """
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized. Set ANTHROPIC_API_KEY.")
        
        try:
            message = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text.strip()
        
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def estimate_cost(self, input_tokens: int, output_tokens: int, 
                     model: Optional[str] = None) -> float:
        """
        Estimate cost for optimization.
        Helpful for showing users how much each optimization costs.
        """
        model = model or self.default_model
        
        if model not in self.models:
            return 0.0
        
        model_info = self.models[model]
        
        # Cost per 1M tokens, convert to actual usage
        input_cost = (input_tokens / 1_000_000) * model_info['input_cost']
        output_cost = (output_tokens / 1_000_000) * model_info['output_cost']
        
        return input_cost + output_cost
    
    def get_best_model_for_task(self, task_type: str) -> str:
        """
        Recommend best model for specific task.
        
        Different models excel at different things.
        """
        recommendations = {
            'style_preservation': 'claude-3-5-sonnet-20241022',  # Claude best at tone
            'speed': 'gpt-3.5-turbo',  # Fastest
            'quality': 'gpt-4o',  # Best overall
            'budget': 'gpt-3.5-turbo',  # Cheapest
            'long_resume': 'claude-3-5-sonnet-20241022'  # 200K context window
        }
        
        recommended = recommendations.get(task_type, self.default_model)
        
        # Check if recommended model is available
        available = self.get_available_models()
        if recommended in available:
            return recommended
        
        # Fallback to default
        return self.default_model
    
    def get_model_info(self, model: Optional[str] = None) -> Dict:
        """Get information about a specific model"""
        model = model or self.default_model
        return self.models.get(model, {})


# Example usage:
"""
optimizer = MultiModelOptimizer()

# Use default model (gpt-4o)
result = optimizer.optimize_text(
    prompt="Enhance this bullet: Led team of engineers",
    system_prompt="You are a resume writer",
    temperature=0.5
)

# Use specific model
result = optimizer.optimize_text(
    prompt="...",
    system_prompt="...",
    model="claude-3-5-sonnet-20241022"  # Use Claude for style preservation
)

# Check available models
available = optimizer.get_available_models()
print(f"Available models: {list(available.keys())}")

# Estimate cost
cost = optimizer.estimate_cost(input_tokens=500, output_tokens=200, model="gpt-4o")
print(f"Estimated cost: ${cost:.4f}")
"""
