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


def build_algorithm_params(args):
    """
    Build a dictionary of parameters for each algorithm based on the command-line arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        dict: A dictionary where the key is the algorithm name and the value is another
              dictionary of parameters specific to that algorithm.
    """
    params = {}

    for arg, value in vars(args).items():
        if value is not None:
            # Split arguments that follow the "algorithm_param" pattern
            if "_" in arg:
                algo_name, param_name = arg.split("_", 1)
                if algo_name not in params:
                    params[algo_name] = {}
                params[algo_name][param_name] = value

    return params
