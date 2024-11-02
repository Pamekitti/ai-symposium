import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add src to Python path
SRC_PATH = Path(__file__).parent / "src"
sys.path.append(str(SRC_PATH))

from symposium.core import Symposium, DebateConfig

def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return

    # Create debate configuration
    config = DebateConfig(
        topic="Should artificial intelligence be regulated?",
        pro_position="AI regulation is necessary for safety and ethical development",
        con_position="Regulation would stifle innovation and technological progress",
        max_turns=10
    )

    print("\n🎭 AI SYMPOSIUM")
    print("=" * 80)
    print("Initializing debate session...")

    # Initialize and run debate
    try:
        symposium = Symposium()
        symposium.setup_debate(config)
        
        opening_prompt = """
        Welcome to today's debate on AI regulation. We'll explore both the potential 
        benefits and risks of regulatory frameworks for artificial intelligence 
        development. Let's begin with opening statements from each side.
        """
        
        result = symposium.run_debate(opening_prompt)
        
    except Exception as e:
        print(f"\n❌ Error running debate: {e}")

if __name__ == "__main__":
    main()