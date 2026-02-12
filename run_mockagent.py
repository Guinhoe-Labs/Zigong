from models.MockAgent import MockPlayerAgent, MockMasterAgent
from models.MockEnvironment import MockEnvironment
from configs.Configs import OpenAIConfig, EnvironmentConfig, OrchestratorConfig, RewardConfig, TeamConfig
from Orchestrator import Orchestrator
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

# --- CONFIGURATION ---
MOCK_GUESSES = ["LEMON", "D", "HAND"] # Sequence of guesses to make
MOCK_HINT_WORD = "COLD"
MOCK_HINT_NUMBER = 2

# Define Team Configs
player_agent = MockPlayerAgent(guesses_sequence=MOCK_GUESSES)
master_agent = MockMasterAgent(hint_word=MOCK_HINT_WORD, hint_number=MOCK_HINT_NUMBER)

TEAM_CONFIG = TeamConfig(
    master_model=master_agent,
    player_models=[player_agent]
)

# Define Orchestrator Config (still needed for structure, though env ignored by MockEnv)
ORCHESTRATOR_CONFIG = OrchestratorConfig(
    team_configs=[TEAM_CONFIG], 
    env_config=EnvironmentConfig(
        teams=1, 
        max_words=25,
        word_list_file="./content/mock_wordlist.txt"
    ),
    reward_config=RewardConfig(),
)

if __name__ == "__main__":
    orchestrator = Orchestrator(ORCHESTRATOR_CONFIG)
    
    # Inject Mock Environment
    orchestrator.environment = MockEnvironment()
    
    print(f"Starting run with MockPlayerAgent and MockEnvironment. Guesses: {MOCK_GUESSES}")
    result = orchestrator.run_episode(limit=10)
    
    print("Episode Result:", result["total_steps"], "steps")
    
    run_id = str(uuid.uuid4())
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    orchestrator.save_run_log(f"{output_dir}/mock_run_{run_id}.json", run_id)
    print(f"Run complete. Log saved to {output_dir}/mock_run_{run_id}.json")
