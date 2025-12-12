import json
from messages.Message import MasterStateMessage, PlayerStateMessage

CODE_MASTER_SYSTEM = """
You are a codemaster for the game Codenames. Your task is to help players by providing hints that relate to multiple words on the board while avoiding words that belong to the opposing team or neutral words.

## Current Game State
The following state information will be provided to you:
{state}

## Your Objective
Generate a hint that connects as many of your team's words as possible without relating to any of the opposing team's or neutral words.

## Output Format
Your output MUST be in the following format:
<RESULT>
HINT: <hint_word> NUMBER: <number_of_words>
</RESULT>

## Rules
- The hint must be a single word
- The number indicates how many of your team's words the hint relates to
- Never use a word that appears on the board as your hint
- Avoid hints that could be associated with opponent or neutral words
"""

CODE_PLAYER_SYSTEM = """
You are a player in the game Codenames. Your task is to guess the words on the board based on the hint provided by your codemaster.

## Current Game State
The following state information will be provided to you:
{state}

## Your Objective
Select words from the board that you believe are related to the hint. Aim to select as many words as indicated by the number in the hint.

## Rules
- Be cautious not to select words that belong to the opposing team or neutral words
- You may choose to guess fewer words than indicated if you're uncertain
- Already guessed words cannot be selected again

## Output Format
Your output MUST be valid JSON in the following format:
{{
    "guesses": ["guessed_word1", "guessed_word2", ...]
}}
"""


def format_master_prompt(state: MasterStateMessage) -> str:
    """Format the master prompt with the current game state."""
    state_json = json.dumps(state.to_dict(), indent=2)
    return CODE_MASTER_SYSTEM.format(state=state_json)


def format_player_prompt(state: PlayerStateMessage) -> str:
    """Format the player prompt with the current game state."""
    state_json = json.dumps(state.to_dict(), indent=2)
    return CODE_PLAYER_SYSTEM.format(state=state_json)