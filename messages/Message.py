from dataclasses import dataclass

@dataclass
class MasterStateMessage:
    team_words: list
    opponent_words: list
    neutral_words: list

    def to_dict(self):
        return {
            "team_words": self.team_words,
            "opponent_words": self.opponent_words,
            "neutral_words": self.neutral_words
        }
    
@dataclass
class PlayerStateMessage:
    hint_word: str
    hint_number: int
    board: list
    guessed_words: list

    def to_dict(self):
        return {
            "hint": {
                "word": self.hint_word,
                "number": self.hint_number
            },
            "board": self.board,
            "guessed_words": self.guessed_words
        }
    
@dataclass
class MasterActionMessage:
    hint_word: str
    hint_number: int

    def to_dict(self):
        return {
            "hint_word": self.hint_word,
            "hint_number": self.hint_number
        }
        
@dataclass
class PlayerActionMessage:
    guesses: list

    def to_dict(self):
        return {
            "guesses": self.guesses
        }