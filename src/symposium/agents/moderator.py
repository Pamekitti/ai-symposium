from swarm.swarm import Agent, Result
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def create_moderator(base_model: str, pro_agent: Agent, con_agent: Agent) -> Agent:
    """Create and return a moderator agent."""
    
    def moderator_instructions(context_variables: Dict) -> str:
        phase = context_variables.get("phase", "opening")
        topic = context_variables.get("topic", "")
        logger.debug(f"Generating moderator instructions for phase: {phase}, topic: {topic}")
        
        return f"""You are the debate moderator for a discussion on: {topic}

        Current phase: {phase}

        Your responsibilities:
        1. Guide the debate through its phases
        2. Ensure speakers remain civil and on-topic
        3. Manage speaking turns fairly
        4. Enforce time limits
        5. Provide summaries between phases
        6. Call for conclusion when appropriate

        Phase-specific instructions:
        - OPENING: Introduce the topic and speakers
        - DISCUSSION: Facilitate back-and-forth dialogue
        - REBUTTAL: Allow speakers to address counterarguments
        - CLOSING: Call for final statements
        - SUMMARY: Provide comprehensive debate summary

        Use the following functions to manage the debate:
        - call_pro_speaker(): Give the floor to the pro position speaker
        - call_con_speaker(): Give the floor to the con position speaker
        - advance_phase(): Move to the next debate phase
        - conclude_debate(): End the debate and provide final summary
        """

    def call_pro_speaker() -> Agent:
        logger.debug("Transferring control to pro speaker")
        return pro_agent

    def call_con_speaker() -> Agent:
        logger.debug("Transferring control to con speaker")
        return con_agent

    def advance_phase(context_variables: Dict) -> Result:
        """Advance the debate to the next phase."""
        current_phase = context_variables.get("phase", "opening")
        phases = ["opening", "discussion", "rebuttal", "closing", "summary"]
        current_index = phases.index(current_phase)
        
        logger.info(f"Advancing from phase: {current_phase}")
        
        if current_index + 1 < len(phases):
            next_phase = phases[current_index + 1]
            logger.info(f"Moving to next phase: {next_phase}")
            return Result(
                value=f"Moving to {next_phase} phase",
                context_variables={"phase": next_phase}
            )
        logger.info("All phases completed, preparing to conclude")
        return Result(
            value="Debate phases completed",
            context_variables={"should_conclude": True}
        )

    def conclude_debate() -> Result:
        """End the debate and provide final summary."""
        logger.info("Concluding debate")
        return Result(
            value="Debate concluded",
            context_variables={"concluded": True}
        )

    return Agent(
        name="Moderator",
        instructions=moderator_instructions,
        functions=[call_pro_speaker, call_con_speaker, advance_phase, conclude_debate],
        model=base_model
    ) 