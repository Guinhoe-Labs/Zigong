import json
from messages.Message import MasterStateMessage, PlayerStateMessage

REASONING_MASTER_SYSTEM = """
You are a highly intelligent codemaster for the game Codenames.
Your goal is to win the game by connecting your team's words with clever, safe hints.

## Game State
{state}

## Task
1. Analyze the board deeply. Identify clear semantic clusters among your team's words.
2. Check strictly against opponent and neutral words. A hint is INVALID if it relates to any of them.
3. Formulate a hint that connects the maximum number of your team's words safely.
4. Explain your reasoning process step-by-step before deciding on the final hint.

## Output Format
You must output your internal thought process and the final action.
Strictly follow and use the following structure:

<THOUGHT>
[Detailed analysis of word associations, potential risks, and trade-offs]
</THOUGHT>

<RESULT>
HINT: <word> NUMBER: <count>
</RESULT>
"""

REASONING_PLAYER_SYSTEM = """
You are a brilliant player in the game Codenames.
Your goal is to correctly identify your team's words based on the codemaster's hint.

## Game State
{state}

## Task
1. Analyze the hint word and its number. What possible meanings does it have?
2. Evaluate every visible word on the board against the hint.
3. Assign a probability or strength of connection to each board word.
4. Select the best matching words, up to the number specified by the hint. Avoid wild guesses.
5. Explain your reasoning process step-by-step.

## Output Format
You must output your internal thought process and the final guesses.
Use the following structure:

<THOUGHT>
[Detailed analysis of the hint and its connection to each board word]
</THOUGHT>

<RESULT>
{{
    "guesses": ["word1", "word2"...]
}}
</RESULT>
"""

def format_reasoning_master_prompt(state: MasterStateMessage) -> str:
    """Format the master prompt with the current game state."""
    state_json = json.dumps(state.to_dict(), indent=2)
    return REASONING_MASTER_SYSTEM.format(state=state_json)

def format_reasoning_player_prompt(state: PlayerStateMessage) -> str:
    """Format the player prompt with the current game state."""
    state_json = json.dumps(state.to_dict(), indent=2)
    return REASONING_PLAYER_SYSTEM.format(state=state_json)


CONSENSUS_CROSS_POLLINATION_SYSTEM = """
You are a brilliant player in the game Codenames.
You have generated an initial guess, but now you have access to the thoughts of your teammates.

## Original Hint
{hint}

## Your Previous Thought
{previous_thought}

## Teammate Thoughts
{teammate_thoughts}

## Task
1. Review your teammates' reasoning. Do they see connections you missed? Are their associations stronger?
2. Re-evaluate your own choices. Are there risks you ignored?
3. Synthesize the best parts of all reasoning to form a new, refined plan.
4. Explain your updated reasoning process step-by-step.

## Output Format
You must output your internal thought process and the final guesses.
Use the following structure:

<THOUGHT>
[Detailed analysis of teammate feedback and refined reasoning]
</THOUGHT>

<RESULT>
{{
    "guesses": ["word1", "word2"...]
}}
</RESULT>
"""

CONSENSUS_JUDGE_SYSTEM = """
You are the Lead Judge for a Codenames team.
Your goal is to make the final decision on which words to guess.

## Original Hint
{hint}

## Team Proposals
{team_proposals}

## Task
1. Analyze the different proposals from your team.
2. Identify the most robust and safe reasoning.
3. Select the best set of words to guess.
4. Explain why you chose this set over the others.

## Output Format
You must output your internal thought process and the final guesses.
Use the following structure:

<THOUGHT>
[Detailed comparison of proposals and final decision logic]
</THOUGHT>

<RESULT>
{{
    "guesses": ["word1", "word2"...]
}}
</RESULT>
"""

def format_cross_pollination_prompt(hint: str, previous_thought: str, teammate_thoughts: str) -> str:
    return CONSENSUS_CROSS_POLLINATION_SYSTEM.format(
        hint=hint,
        previous_thought=previous_thought,
        teammate_thoughts=teammate_thoughts
    )

def format_judge_prompt(hint: str, team_proposals: str) -> str:
    return CONSENSUS_JUDGE_SYSTEM.format(
        hint=hint,
        team_proposals=team_proposals
    )
