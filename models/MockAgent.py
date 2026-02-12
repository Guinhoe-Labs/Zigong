
from typing import List
from messages.Message import PlayerActionMessage, MasterActionMessage, PlayerDiscussionMessage

class MockPlayerAgent:
    def __init__(self, guesses_sequence: List[str] = None):
        """
        guesses_sequence: List of words to guess in order.
        """
        self.guesses = guesses_sequence if guesses_sequence else []
        self.current_index = 0
        print("MockPlayerAgent initialized")

    def generate_player_action(self, prompt: str) -> tuple[PlayerActionMessage, str]:
        if self.current_index < len(self.guesses):
            guess = self.guesses[self.current_index]
            self.current_index += 1
            # Return single guess as per new protocol
            return PlayerActionMessage(guesses=[guess]), "<RESULT>Mocked</RESULT>"
        else:
            return PlayerActionMessage(guesses=[]), "No more guesses"
            
    def generate_player_discussion(self, prompt: str, identifier: str, history: List[str]) -> tuple[PlayerDiscussionMessage, str]:
        return PlayerDiscussionMessage(response="Mock discussion", guesses=[]), "Mock discussion"
    
    def get_config(self):
        return {}

class MockMasterAgent:
    def __init__(self, hint_word: str, hint_number: int):
        self.hint_word = hint_word
        self.hint_number = hint_number
        print("MockMasterAgent initialized")
        
    def generate_master(self, prompt: str) -> tuple[MasterActionMessage, str]:
        return MasterActionMessage(hint_word=self.hint_word, hint_number=self.hint_number), "<RESULT>Mocked</RESULT>"
    
    def get_config(self):
        return {}
