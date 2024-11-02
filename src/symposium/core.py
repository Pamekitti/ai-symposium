from swarm.swarm import Swarm
from typing import Dict, Optional
import logging
import json

from .config.debate import DebateConfig, DebatePhase
from .agents.moderator import create_moderator
from .agents.debater import create_debater
from .utils.logging import setup_logging

logger = setup_logging()

def print_debate_message(role: str, message: str, phase: str = None):
    """Print debate messages in a formatted way"""
    print("\n" + "="*80)
    print(f"🎙️ {role.upper()}")
    if phase:
        print(f"📍 Phase: {phase}")
    print("-"*80)
    print(message.strip())
    print("="*80 + "\n")

class Symposium:
    """Main debate orchestration class."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize a new Symposium instance.
        
        Args:
            model: The name of the language model to use
        """
        logger.info(f"Initializing Symposium with model: {model}")
        self.client = Swarm()
        self.base_model = model
        self.pro_agent = None
        self.con_agent = None
        self.config = None
        self.context = {}
        self.moderator = None  # Will be initialized in setup_debate

    def setup_debate(self, config: DebateConfig) -> None:
        """Initialize a new debate session with the given configuration.
        
        Args:
            config: DebateConfig instance containing debate settings
            
        Raises:
            ValueError: If debate is already in progress
        """
        if self.config is not None:
            raise ValueError("A debate is already in progress. Complete or reset it first.")
        
        logger.info(f"Setting up debate on topic: {config.topic}")
        self.config = config
        self.pro_agent = create_debater("pro", "pro", self.base_model, self.moderator)
        self.con_agent = create_debater("con", "con", self.base_model, self.moderator)
        self.moderator = create_moderator(self.base_model, self.pro_agent, self.con_agent)
        
        # Initialize context variables
        self.context = {
            "topic": config.topic,
            "pro_position": config.pro_position,
            "con_position": config.con_position,
            "phase": DebatePhase.OPENING.value,
            "turn_count": 0,
            "style": config.style,
            "concluded": False
        }
        logger.debug(f"Initialized debate context: {json.dumps(self.context, indent=2)}")

    def run_debate(self, opening_prompt: str) -> Dict:
        """Execute the debate session."""
        logger.info("Starting debate execution")
        
        # Print debate initialization
        print("\n🎭 DEBATE INITIALIZATION")
        print(f"Topic: {self.config.topic}")
        print(f"Pro Position: {self.config.pro_position}")
        print(f"Con Position: {self.config.con_position}")
        print("\n" + "="*80 + "\n")
        
        messages = [{
            "role": "user",
            "content": opening_prompt
        }]
        print_debate_message("Moderator", opening_prompt, "Setup")

        while not self.context.get("concluded", False):
            try:
                # Log current state
                logger.debug(f"Turn {self.context['turn_count']}, Phase: {self.context['phase']}")
                
                # Check turn limit
                if self.context["turn_count"] >= self.config.max_turns:
                    logger.info("Reached maximum turns, initiating conclusion")
                    self.context["should_conclude"] = True
                    print("\n⚠️ Maximum turns reached, concluding debate...\n")

                # Run the next turn
                response = self.client.run(
                    agent=self.moderator,
                    messages=messages,
                    context_variables=self.context,
                    max_turns=1,
                    model_override=self.base_model
                )
                
                speaker_response = self.client.run(
                    agent=response.agent,
                    messages=response.messages,
                    context_variables=self.context,
                    max_turns=1,
                    model_override=self.base_model
                )
                        
                # Update messages and print speaker's response
                messages = speaker_response.messages
                if speaker_response.messages[-1].get("content"):
                    print_debate_message(
                        speaker_response.agent.name,
                        speaker_response.messages[-1]["content"],
                        self.context["phase"]
                    )

                # Update state
                self.context.update(response.context_variables)
                self.context["turn_count"] += 1

                # Handle phase completion
                if self.context.get("should_conclude", False):
                    logger.info("Generating final summary")
                    print("\n🏁 Generating final summary...\n")
                    
                    final_response = self.client.run(
                        agent=self.moderator,
                        messages=messages,
                        context_variables=self.context,
                        max_turns=1
                    )
                    
                    if final_response.messages[-1].get("content"):
                        print("\n📋 DEBATE SUMMARY")
                        print("=" * 80)
                        print(final_response.messages[-1]["content"])
                        print("=" * 80 + "\n")
                    
                    messages = final_response.messages
                    logger.info("Debate concluded successfully")
                    break

            except Exception as e:
                logger.error(f"Error during debate execution: {str(e)}", exc_info=True)
                print(f"\n❌ Error during debate: {str(e)}\n")
                raise

        # Print debate statistics
        print("\n📊 DEBATE STATISTICS")
        print(f"Total Turns: {self.context['turn_count']}")
        print(f"Final Phase: {self.context['phase']}")
        print("=" * 80 + "\n")

        result = {
            "topic": self.config.topic,
            "messages": messages,
            "turns": self.context["turn_count"],
            "final_summary": messages[-1].get("content", "No summary available")
        }
        
        logger.info(f"Debate completed in {result['turns']} turns")
        return result