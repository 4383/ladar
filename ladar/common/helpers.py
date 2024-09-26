import logging


def is_verbose(level="INFO"):
    """
    Helper function to check the current logging level.
    Returns True if the current logging level is greater than or equal to the provided level.
    """
    logger = logging.getLogger()
    level_value = logging.getLevelName(level.upper())

    return logger.isEnabledFor(level_value)
