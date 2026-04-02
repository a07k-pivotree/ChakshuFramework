# This file sets up the logger for the entire framework.
# It creates one log file per test run, named with date, time and test module name.
# Usage from anywhere: from utils.logger import get_logger
#                      logger = get_logger(__name__)

import logging
import os
from datetime import datetime


def setup_logger(test_module_name: str) -> logging.Logger:
    """
    Creates and returns a logger that writes to:
      - logs/YYYY-MM-DD_HH-MM-SS_<test_module_name>.log  (file)
      - terminal (console)

    Called once from conftest.py at the start of each session.
    """

    # ── Build log filename with timestamp + test module name ──────────────────
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{timestamp}_{test_module_name}.log"

    # ── Make sure logs/ folder exists ─────────────────────────────────────────
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_filepath = os.path.join(logs_dir, log_filename)

    # ── Create logger ─────────────────────────────────────────────────────────
    logger = logging.getLogger("chakshu_framework")
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # ── Format: [2025-06-10 14:30:22] [INFO] message ─────────────────────────
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── File handler — writes to logs/ folder ────────────────────────────────
    file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # ── Console handler — shows in terminal during run ────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "chakshu_framework") -> logging.Logger:
    """
    Returns the existing logger from anywhere in the project.
    Always call setup_logger() first from conftest — this just retrieves it.
    """
    return logging.getLogger("chakshu_framework")