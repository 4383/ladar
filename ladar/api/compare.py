import concurrent.futures
import importlib
import os

from ladar.common.helpers import discover_modules


def load_algorithms():
    """
    Dynamically load all comparison algorithms from the 'ladar/api/algorithms' directory.

    Returns:
        dict: A dictionary of algorithm names mapped to their comparison functions.
    """
    algorithms_dir = os.path.dirname(__file__) + "/algorithms"
    algorithm_modules = discover_modules(algorithms_dir)

    algorithms = {}
    for module_name in algorithm_modules:
        try:
            module = importlib.import_module(f"ladar.api.algorithms.{module_name}")
            if hasattr(module, "compare"):
                algorithms[module_name] = module.compare
        except ImportError as e:
            print(f"Failed to import algorithm {module_name}: {e}")

    return algorithms


def compare_structures(structures: list, algorithms=None) -> dict:
    """
    Compare multiple API structures using specified algorithms.

    Args:
        structures (list): A list of API structures to compare.
        algorithms (list): List of algorithm names to use for comparison. Defaults to all available.

    Returns:
        dict: A dictionary containing the comparison results for each algorithm.
    """
    available_algorithms = load_algorithms()

    if algorithms is None:
        algorithms = available_algorithms.keys()

    results = {}

    def compare_with_algorithm(algorithm):
        """Effectue la comparaison avec un algorithme spécifique."""
        return algorithm, available_algorithms[algorithm](structures)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_algorithm = {
            executor.submit(compare_with_algorithm, algo): algo
            for algo in algorithms
            if algo in available_algorithms
        }

        for future in concurrent.futures.as_completed(future_to_algorithm):
            algorithm = future_to_algorithm[future]
            try:
                algo_name, result = future.result()
                results[algo_name] = result
            except Exception as e:
                results[algorithm] = f"Comparison failed with error: {e}"

    return results
