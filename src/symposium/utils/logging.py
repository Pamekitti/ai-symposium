import logging
from datetime import datetime

def setup_logging():
    """Configure logging with both console and file handlers."""
    logger = logging.getLogger(__name__)
    
    # Configure basic logging
    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Add file handler for debug logs
    log_filename = f'debate_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    debug_handler = logging.FileHandler(log_filename)
    debug_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    debug_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)
    
    return logger 