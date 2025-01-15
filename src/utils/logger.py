import logging
import os
from pathlib import Path

def setup_logger():
    # Create logs directory in project root
    log_dir = Path(__file__).parents[2] / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / 'bestbuy_monitor.log'
    
    logger = logging.getLogger('BestBuyMonitor')
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()
