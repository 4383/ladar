import argparse
import logging
import textwrap

from ladar.api.compare import load_algorithms
from ladar.api.pipeline import parse, run
from ladar.common.helpers import build_algorithm_params
from ladar.common.io import load, save

logger = logging.getLogger(__name__)

command_description = """
Compare multiple API structures using a pipeline of algorithms or a single algorithm.
"""

long_description = """
The 'compare' command allows you to compare multiple API structures using either:
1. A pipeline of algorithms executed sequentially.
2. A single algorithm in isolation with its specific parameters.

The comparison results will be saved in the specified output file.
"""


def add_arguments(parser):
    """
    Adds argument options to the compare command parser. The parser is updated to handle two modes:
    - Pipeline mode, where a sequence of algorithms is executed in a defined order.
    - Single algorithm mode, where only one algorithm is run with specific parameters.

    Args:
        parser (argparse.ArgumentParser): The parser to which arguments are added.

    Arguments:
        --structures (list):
            - A list of paths to the structures to compare. At least two structures are required.

        --pipeline (str, optional):
            - A string specifying a pipeline of algorithms, formatted as: stage:Algorithm(params).
              Each step is executed sequentially with the output of one step passed as input to the next.

        --output (str, required):
            - The path to the file where comparison results will be saved.
              Supported formats are 'toml', 'yaml', and 'json'.

        --<algorithm-specific-args> (optional):
            - Individual parameters for algorithms, available only when running a single algorithm.

    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    available_algorithms = load_algorithms()

    algorithm_help = "Specify a pipeline of algorithms.\nAvailable algorithms:\n"

    # Ajouter chaque algorithme avec sa catégorie (standardisée via l'enum) dans l'aide
    for algorithm_name, algorithm_info in available_algorithms.items():
        algorithm_help += (
            f"- {algorithm_name} (category: {algorithm_info['category']})\n"
        )

    algorithm_help += (
        "Example: --pipeline normalize:minmaxscaler,extract:tfidf,cluster:dbscan"
    )

    # Add argument for structures (input files)
    parser.add_argument(
        "--structures",
        nargs="+",
        required=True,
        help="A list of paths to the structures to compare (at least two required).",
    )

    # Add argument for pipeline mode
    parser.add_argument(
        "--pipeline",
        required=False,
        help=algorithm_help,
    )

    # Add argument for output
    parser.add_argument(
        "--output",
        required=True,
        help="Specify the output file where the comparison results will be saved (e.g., 'output.yaml').",
    )

    # Add algorithm-specific arguments dynamically
    for algorithm_name, algorithm_info in available_algorithms.items():
        algorithm_info["class"].add_arguments(parser)


def main(args):
    """
    Main function for the 'compare' command. It handles two modes:
    1. **Pipeline mode**: When `--pipeline` is specified, the algorithms are executed sequentially.
    2. **Single algorithm mode**: When `--pipeline` is not specified, a single algorithm is executed.

    Args:
        args (argparse.Namespace): The parsed arguments from the command line.
    """
    if len(args.structures) < 2:
        logger.error("At least two structures are required for comparison.")
        return

    structures = []
    for structure_path in args.structures:
        try:
            structure = load(structure_path)["structure"]
            structures.append(structure)
        except Exception as e:
            logger.error(f"Failed to load structure {structure_path}: {e}")
            return

    if args.pipeline:
        pipeline_steps = parse(args.pipeline)
        params = build_algorithm_params(args)
        comparison_results = run(pipeline_steps, structures, params)
    else:
        logger.error("No pipeline specified. Please provide a valid pipeline.")
        return

    try:
        save(args.output, comparison_results)
        print(f"Comparison results saved to {args.output}")
    except ValueError as e:
        logger.error(f"Error saving comparison results: {e}")
