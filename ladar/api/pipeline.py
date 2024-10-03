import ast
import importlib
import logging
import re

from ladar.api.compare import load_algorithms

logger = logging.getLogger(__name__)


def parse_step(step_str):
    """
    Parse a pipeline step string to extract the algorithm name.

    Args:
        step_str (str): A string representing a step in the pipeline, e.g. 'normalize:minmaxscaler'.

    Returns:
        str: The name of the algorithm in lowercase.

    Raises:
        ValueError: If the step format is invalid.
    """
    # Simple regex to capture the algorithm name (without params)
    match = re.match(r"(\w+):(\w+)", step_str)

    if match:
        stage, algorithm_name = match.groups()
        return algorithm_name.lower()

    else:
        raise ValueError(f"Invalid step format: {step_str}")


def parse(pipeline_str):
    """
    Parse the pipeline string into individual algorithm steps.

    Args:
        pipeline_str (str): The pipeline string provided by the user, e.g., 'normalize:minmaxscaler,cluster:dbscan'.

    Returns:
        list: A list of pipeline steps in the correct order.
    """

    available_algorithms = load_algorithms()
    standardized_algorithms = {
        name.lower(): module["class"] for name, module in available_algorithms.items()
    }  # Ensure we are working with the algorithm class itself

    steps = []
    for step_str in pipeline_str.split(","):
        algorithm_name = parse_step(step_str)

        algorithm_name = algorithm_name.lower()
        if algorithm_name not in standardized_algorithms:
            raise ValueError(
                f"Algorithm '{algorithm_name}' not found in available algorithms: {', '.join(standardized_algorithms.keys())}"
            )

        steps.append(
            {
                "algorithm": standardized_algorithms[algorithm_name]
            }  # Store the class itself
        )

    return steps


def run(pipeline_steps, structures, params):
    """
    Execute the specified pipeline of algorithms on the given structures.

    Args:
        pipeline_steps (list): List of pipeline steps with algorithm names.
        structures (list): A list of input structures to compare.
        params (dict): Parameters for each algorithm.

    Returns:
        dict: The final results after processing all pipeline steps.
    """
    data = structures

    for step in pipeline_steps:
        algorithm_class = step["algorithm"]  # Directly access the class
        algorithm_name = algorithm_class.__name__.lower()  # Get the class name
        algorithm_params = params.get(
            algorithm_name, {}
        )  # Get the algorithm parameters

        # Instantiate the algorithm with the given parameters
        algorithm = algorithm_class(**algorithm_params)

        # Execute the fit_transform (or transform) method on the data
        try:
            if hasattr(algorithm, "fit_transform"):
                data = algorithm.fit_transform(data)
            elif hasattr(algorithm, "transform"):
                data = algorithm.transform(data)
            else:
                raise ValueError(
                    f"Algorithm {algorithm_name} does not support transformation."
                )
        except Exception as e:
            raise RuntimeError(f"Error running {algorithm_name}: {e}")

    return data


def load_algorithm_by_name(name):
    """
    Load the algorithm class by its name.

    Args:
        name (str): The name of the algorithm (e.g., 'DBSCAN', 'MinMaxScaler').

    Returns:
        class: The algorithm class if found, None otherwise.
    """
    try:
        module = importlib.import_module(f"ladar.algorithms.{name.lower()}")
        return getattr(module, name)
    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to load algorithm {name}: {e}")
        return None
