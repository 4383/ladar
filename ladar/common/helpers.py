import logging
import os


def is_verbose(level="INFO"):
    """
    Helper function to check the current logging level.
    Returns True if the current logging level is greater than or equal to the provided level.
    """
    logger = logging.getLogger()
    level_value = logging.getLevelName(level.upper())

    return logger.isEnabledFor(level_value)


def discover_modules(directory):
    """
    Discover all Python modules in the given directory.

    Args:
        directory (str): Path to the directory where Python modules are located.

    Returns:
        list: A list of module names without file extensions.
    """
    modules = []
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            modules.append(filename[:-3])
    return modules
