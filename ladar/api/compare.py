import concurrent.futures
import importlib
import logging
import os
import pkgutil

from ladar.api.algorithms.base import AlgorithmCategory, BaseAlgorithm
from ladar.common.helpers import discover_modules

logger = logging.getLogger(__name__)


def load_algorithms():
    """
    Dynamically load and validate all algorithms in the ladar/api/algorithms directory.

    Returns:
        dict: A dictionary where keys are algorithm names and values are their corresponding classes and categories.
    """
    algorithms = {}

    logger.debug("Starting to load algorithms from 'ladar/api/algorithms'")

    for _, module_name, _ in pkgutil.iter_modules(["ladar/api/algorithms"]):
        logger.debug(f"Attempting to load module: {module_name}")
        try:
            module = importlib.import_module(f"ladar.api.algorithms.{module_name}")
        except ImportError as e:
            logger.debug(f"Error importing module {module_name}: {e}")
            continue

        # Find the algorithm class in the module, allowing different class names
        algorithm_class = None
        for name, cls in vars(module).items():
            if (
                isinstance(cls, type)
                and issubclass(cls, BaseAlgorithm)
                and cls is not BaseAlgorithm
            ):
                algorithm_class = cls
                break

        if algorithm_class:
            logger.debug(f"Found algorithm class: {algorithm_class}")
            if isinstance(algorithm_class.category, AlgorithmCategory):
                algorithms[module_name] = {
                    "class": algorithm_class,
                    "category": algorithm_class.category.value,
                }
                logger.debug(
                    f"Algorithm {module_name} loaded successfully with category: {algorithm_class.category.value}"
                )
            else:
                logger.debug(f"Algorithm {module_name} has an invalid category.")
        else:
            logger.debug(f"No valid algorithm class found in module {module_name}.")

    logger.debug(
        f"Finished loading algorithms. Total algorithms loaded: {len(algorithms)}"
    )

    return algorithms
