
import unittest
from unittest.mock import MagicMock
import sys

# Mock dependencies
sys.modules["langgraph"] = MagicMock()
sys.modules["langgraph.graph"] = MagicMock()
sys.modules["core.CrossTalk"] = MagicMock()

from Orchestrator import Orchestrator
from messages.Message import MasterActionMessage, PlayerActionMessage

class TestNoBonusGuess(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock()
        self.mock_config.env_config = {"teams": 1, "max_words": 25, "test_flag": True}
        self.mock_config.team_configs = [MagicMock()]
        self.mock_config.team_configs[0].master_model = MagicMock()
        self.mock_config.team_configs[0].player_models = [MagicMock()]
        self.mock_config.reward_config = MagicMock()

        self.orchestrator = Orchestrator(self.mock_config)
        self.orchestrator.environment = MagicMock()
        
    def test_loop_stops_at_hint_number(self):
        # Hint "Fruit" 2
        m_action = MasterActionMessage(hint_word="Fruit", hint_number=2)
        self.orchestrator.teams[1]["master_model"].generate_master.return_value = (m_action, "thought")
        
        self.orchestrator.environment.handle_master_action.return_value = {
            "success": True,
            "hint": {"word": "Fruit", "number": 2}
        }
        
        # Mock get_player_state to return valid data for json serialization
        self.orchestrator.environment.get_player_state.return_value = {
            "board": ["Apple", "Banana", "Cherry", "Dog"],
            "guessed_words_log": []
        }
        
        # 3 Correct Guesses provided by model
        self.orchestrator.teams[1]["player_models"][0].generate_player_action.side_effect = [
            (PlayerActionMessage(guesses=["Apple"]), "thought"),
            (PlayerActionMessage(guesses=["Banana"]), "thought"),
            (PlayerActionMessage(guesses=["Cherry"]), "thought") 
        ]
        
        # Environment confirms they are correct
        self.orchestrator.environment.handle_player_action.side_effect = [
            {"success": True, "results": [{"word": "Apple", "result": "correct"}]},
            {"success": True, "results": [{"word": "Banana", "result": "correct"}]},
            {"success": True, "results": [{"word": "Cherry", "result": "correct"}]}
        ]
        
        result = self.orchestrator.team_step(1)
        
        # Verify loop stopped after 2 guesses (Hint Number), ignoring the 3rd potential guess
        self.assertEqual(self.orchestrator.environment.handle_player_action.call_count, 2)
        self.assertEqual(result["player_action"]["guesses"], ["Apple", "Banana"])

if __name__ == '__main__':
    unittest.main()
