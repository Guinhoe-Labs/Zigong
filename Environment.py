from typing import Any, List

import random

class Environment:
    def __init__(self, config):
        # Game state
        self.teams = config.get("teams", 1)
        self.word_sets = {}

        # Configuration parameters
        self.max_words = config.get("max_words", 25)

        with open(config["word_list_file"], 'r') as f:
            word_list = [line.strip() for line in f.readlines()]
            self._setup_board(word_list)

    def _setup_board(self, word_list: List[str]):
        word_set = random.shuffle(word_list)
        self.board = word_set[:self.max_words]
        if self.teams > 1:
            # Setup for multiple teams
            pass
        else:
            self.word_sets[1] = random.shuffle(self.board)[:8]
        
    def check_win(self):
        if self.teams > 1:
            # Check win conditions for multiple teams
            pass
        else:
            return len(self.word_sets[1]) == 0
        return False
    
    def get_master_state(self):
        return {
            "board": self.board,
            "word_sets": self.word_sets
        }