from Rewards import RewardModule


def test_reward_function_flat_player_result_scoring():
    module = RewardModule()
    event = {
        "environment_state": {"board": ["apple", "banana", "cherry"]},
        "master_result": {
            "success": True,
            "action": {"hint_word": "fruit", "hint_number": 2},
        },
        "player_result": {
            "success": True,
            "results": [
                {"word": "apple", "result": "correct"},
                {"word": "banana", "result": "neutral"},
                {"word": "cherry", "result": "opponent"},
                {"word": "apple", "result": "already_guessed"},
            ],
        },
    }

    master_reward, player_reward = module.reward_function(event)

    assert master_reward == 5
    assert player_reward == -14


def test_reward_function_master_hint_on_board_penalty():
    module = RewardModule()
    event = {
        "environment_state": {"board": ["apple", "banana", "cherry"]},
        "master_result": {
            "success": True,
            "action": {"hint_word": "banana", "hint_number": 1},
        },
        "player_result": {"success": True, "results": []},
    }

    master_reward, player_reward = module.reward_function(event)

    assert master_reward == -8
    assert player_reward == 0


def test_reward_function_format_penalties():
    module = RewardModule()
    event = {
        "environment_state": {"board": ["apple", "banana", "cherry"]},
        "master_result": {"success": False},
        "player_result": {"success": False},
    }

    master_reward, player_reward = module.reward_function(event)

    assert master_reward == -10
    assert player_reward == -10
