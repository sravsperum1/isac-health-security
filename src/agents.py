"""
Agent classes with max_iterations safety guard 
Multi-agent sequential pipeline 
"""
import time
import json
from typing import List, Dict, Any
from openai import AzureOpenAI
from src.tools import TOOLS, TOOL_FUNCTIONS


class Agent:
    """Base agent class with max_iterations safety guardrail"""
    
    def __init__(self, name: str, system_prompt: str, client: AzureOpenAI, model: str,
                 temperature: float = 0.1, max_tokens: int = 800,
                 max_iterations: int = 3, use_tools: bool = False):
        self.name = name
        self.system_prompt = system_prompt
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_iterations = max_iterations  # Safety guardrail
        self.use_tools = use_tools
        self.total_tokens = 0

    def run(self, user_message: str) -> Dict[str, Any]:
        """Execute agent with retry logic and iteration limit"""
        messages = [
            {"role": "system", "content": self.system_prompt[:2000]},
            {"role": "user", "content": user_message[:4000]}
        ]
        
        for iteration in range(self.max_iterations):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }
                
                # Add tools if this agent uses function calling
                if self.use_tools:
                    kwargs["tools"] = TOOLS
                    kwargs["tool_choice"] = "auto"
                
                response = self.client.chat.completions.create(**kwargs)
                response_message = response.choices[0].message
                self.total_tokens += response.usage.total_tokens
                
                # Handle tool calls if present
                if response_message.tool_calls and self.use_tools:
                    messages.append(response_message)
                    for tool_call in response_message.tool_calls:
                        func_name = tool_call.function.name
                        func_args = json.loads(tool_call.function.arguments)
                        func_to_call = TOOL_FUNCTIONS.get(func_name)
                        if func_to_call:
                            tool_result = func_to_call(**func_args)
                            messages.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": func_name,
                                "content": json.dumps(tool_result)
                            })
                    continue
                
                return {
                    "status": "success",
                    "output": response_message.content,
                    "tokens": response.usage.total_tokens,
                    "agent": self.name,
                    "iterations": iteration + 1
                }
                
            except Exception as e:
                if iteration == self.max_iterations - 1:
                    return {"status": "error", "error": str(e), "agent": self.name}
                time.sleep(2 ** iteration)  # Exponential backoff
        
        return {"status": "error", "error": "Max iterations exceeded", "agent": self.name}


class SequentialPipeline:
    """Sequential multi-agent pipeline - output of each becomes input to next"""
    
    def __init__(self, agents: List[Agent], verbose: bool = True):
        self.agents = agents
        self.verbose = verbose
        self.results = {}

    def run(self, initial_input: str) -> Dict[str, Any]:
        """Run agents sequentially with output chaining"""
        current_input = initial_input
        
        for i, agent in enumerate(self.agents):
            if self.verbose:
                print(f"\n[{i+1}/{len(self.agents)}] Running {agent.name}...")
            
            result = agent.run(current_input)
            
            if result["status"] == "error":
                self.results["error"] = result.get("error")
                return self.results
            
            current_input = result["output"]
            self.results[agent.name] = {
                "output": result["output"],
                "tokens": result["tokens"],
                "iterations": result.get("iterations", 1)
            }
            
            if self.verbose:
                print(f"   {agent.name} complete ({result['tokens']} tokens)")
        
        self.results["final_output"] = current_input
        self.results["total_tokens"] = sum(
            v.get("tokens", 0) for v in self.results.values() if isinstance(v, dict)
        )
        
        return self.results