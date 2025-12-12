from abc import ABC, abstractmethod
from pyexpat import model
from typing import Any
from Environment import Environment

import requests

class Orchestrator(ABC):
    def __init__(self, orchestration_config):
        self.environment = Environment(orchestration_config["env_config"])
    
    @abstractmethod
    def get_master_state(self, master_id):
        pass

    @abstractmethod
    def handle_master_action(self, master_id, action: Any):
        pass

    @abstractmethod
    def get_player_state(self, player_id):
        pass

    @abstractmethod
    def handle_player_action(self, player_id, action: Any):
        pass


class OllamaOrchestrator(Orchestrator):
    def __init__(self, config):
        super().__init__(config)
        # Additional setup for Ollama backend

        self.master = config.get("master", None)
        self.player = config.get("player", None)

    def get_master_state(self, master_id):
        # Implementation for Ollama
        pass

    def handle_master_action(self, master_id, action: Any):
        # Implementation for Ollama
        pass

    def get_player_state(self, player_id):
        # Implementation for Ollama
        pass

    def handle_player_action(self, player_id, action: Any):
        # Implementation for Ollama
        pass

    def _query_ollama(self, prompt, model):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            return f"Error querying Ollama: {e}"