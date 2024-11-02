from swarm.swarm import Agent
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def create_debater(position: str, stance: str, base_model: str, moderator: Agent) -> Agent:
    """Create and return a debater agent."""
    
    def speaker_instructions(context_variables: Dict) -> str:
        topic = context_variables.get("topic", "")
        phase = context_variables.get("phase", "opening")
        position_statement = context_variables.get(f"{stance}_position", "")
        
        logger.debug(f"Generating {position} speaker instructions for phase: {phase}")
        
        return f"""You are the {position} speaker, arguing: {position_statement}
        Topic: {topic}
        Current Phase: {phase}

        Phase-specific guidelines:
        - OPENING: Present your main arguments clearly and concisely
        - DISCUSSION: Develop your points with evidence and examples
        - REBUTTAL: Address opposing arguments directly and effectively
        - CLOSING: Summarize your key points convincingly
        - SUMMARY: Listen to final summary

        Important:
        - Speak in clear, natural language
        - Make your points directly without meta-commentary
        - Do not describe your role or actions, just speak your arguments
        - Avoid saying "As the {position} speaker..." - just make your points

        Use return_to_moderator() when you've completed your point.
        """

    def return_to_moderator() -> Agent:
        logger.debug(f"{position} speaker returning control to moderator")
        return moderator

    return Agent(
        name=f"{position.capitalize()} Speaker",
        instructions=speaker_instructions,
        functions=[return_to_moderator],
        model=base_model
    ) 