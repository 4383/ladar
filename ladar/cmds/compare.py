import argparse
import logging
import textwrap

from ladar.api.compare import compare_structures, load_algorithms
from ladar.common.helpers import build_algorithm_params
from ladar.common.io import load, save

logger = logging.getLogger(__name__)

command_description = """
Compare multiple API structures using one or more dynamically discovered algorithms.
"""

long_description = """
The 'compare' command allows you to compare multiple API structures, using one or more dynamically discovered algorithms.
You can specify the algorithms or use all available algorithms by default.
The comparison results will be saved in the specified output file.
"""


def add_arguments(parser):
    """
    Adds the argument options to the compare command parser.

    Args:
        parser (argparse.ArgumentParser): The parser to which arguments are added.

    Arguments:
        --structures (list):
            - A list of paths to the structures to compare.

        --algorithms (list, optional):
            - Specify the algorithms to use for comparison. By default, all discovered algorithms are used.

        --output (str, required):
            - Specify the output file where the comparison results will be saved.
              Supported formats are 'toml', 'yaml', and 'json'.
    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    available_algorithms = load_algorithms()
    algorithm_help = f"Specify the algorithms to use for comparison. Default is all discovered algorithms.\nAvailable algorithms: {', '.join(available_algorithms.keys())}"

    parser.add_argument(
        "--structures",
        nargs="+",
        required=True,
        help="A list of paths to the structures to compare (at least two required).",
    )
    parser.add_argument(
        "--algorithms",
        nargs="+",
        help=algorithm_help,
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Specify the output file where the comparison results will be saved (e.g., 'output.yaml').",
    )
    for algorithm_name, algorithm_module in available_algorithms.items():
        if hasattr(algorithm_module, "add_arguments"):
            algorithm_module.add_arguments(parser)


def main(args):
    if len(args.structures) < 2:
        logger.error("At least two structures are required for comparison.")
        return

    # Charger les structures à comparer
    structures = []
    for structure_path in args.structures:
        try:
            structure = load(structure_path)
            structures.append(structure)
        except Exception as e:
            logger.error(f"Failed to load structure {structure_path}: {e}")
            return

    # Utiliser la nouvelle fonction pour construire les paramètres des algorithmes
    params = build_algorithm_params(args)

    # Exécuter la comparaison
    comparison_results = compare_structures(
        structures, algorithms=args.algorithms, params=params
    )

    # Sauvegarder les résultats de comparaison
    try:
        save(args.output, comparison_results)
        print(f"Comparison results saved to {args.output}")
    except ValueError as e:
        logger.error(f"Error saving comparison results: {e}")
