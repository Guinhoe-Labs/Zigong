
from messages.Message import MasterActionMessage, PlayerActionMessage

class MockEnvironment:
    def __init__(self, config=None):
        print("MockEnvironment initialized")
        self.board = ["LEMON", "ICE", "HAND", "SUN", "MOON"]
        self.word_sets = {
            1: ["LEMON", "ICE"],
            2: ["SUN", "MOON"]
        }
        self.neutral_words = ["HAND"]
        self.guessed_words = []
        self.guessed_words_log = {1: [], 2: []}
        self.current_hint = None
        self.teams = 1

    def get_master_state(self, team_id: int = 1) -> dict:
        return {
            "board": self.board,
            "word_sets": self.word_sets,
            "guessed_words": self.guessed_words,
            "guessed_words_log": self.guessed_words_log.get(team_id, [])
        }

    def handle_master_action(self, action: MasterActionMessage) -> dict:
        self.current_hint = {
            "word": action.hint_word,
            "number": action.hint_number
        }
        return {
            "success": True,
            "hint": self.current_hint
        }

    def get_player_state(self, team_id: int = 1) -> dict:
        return {
            "board": [w for w in self.board if w not in self.guessed_words],
            "guessed_words_log": self.guessed_words_log.get(team_id, [])
        }

    def handle_player_action(self, action: PlayerActionMessage, team_id: int = 1) -> dict:
        results = []
        correct_count = 0
        
        for guess in action.guesses:
            result = ""
            if guess in self.guessed_words:
                 result = "already_guessed"
            elif guess in self.word_sets.get(team_id, []):
                result = "correct"
                correct_count += 1
            elif guess in self.neutral_words:
                result = "neutral"
            elif any(guess in words for tid, words in self.word_sets.items() if tid != team_id):
                result = "opponent"
            else:
                result = "invalid"

            guess_dict = {"word": guess, "result": result}
            results.append(guess_dict)
            self.guessed_words.append(guess)
            self.guessed_words_log[team_id].append(guess_dict)

        return {
            "success": True,
            "results": results,
            "correct_count": correct_count,
            "game_over": self.check_win()
        }

    def check_win(self) -> bool:
        remaining = [w for w in self.word_sets[1] if w not in self.guessed_words]
        return len(remaining) == 0

    def get_winner(self) -> int:
        return 1 if self.check_win() else -1

    def get_game_state(self) -> dict:
        return {
            "board": self.board,
            "word_sets": self.word_sets,
            "neutral_words": self.neutral_words,
            "guessed_words": self.guessed_words
        }
