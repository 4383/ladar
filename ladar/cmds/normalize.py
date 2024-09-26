import argparse
import json
import logging
import os

import toml
import yaml

from ladar.api.normalize import normalize_content
from ladar.common.io import load, save

logger = logging.getLogger(__name__)

command_description = """
Normalize the content of a file by transforming names to lowercase and removing underscores or camel cases.
"""
long_description = """
The 'normalize' command processes the content of a specified file by normalizing names, converting them
to lowercase, removing underscores, and transforming camel case to a flat format.

You can specify an output file where the normalized content will be saved, or by default, the input file
will be overwritten. You can also preview the normalized result without saving it.
"""


def add_arguments(parser):
    """
    Adds the argument options to the normalize command parser.

    Args:
        parser (argparse.ArgumentParser): The parser to which arguments are added.

    Arguments:
        --input (str):
            - Specify the input file to normalize.

        --output (str, optional):
            - Specify the output file where the normalized content will be saved.
              If not provided, the input file will be overwritten.

        --preview (bool, optional):
            - If enabled, shows the normalized content without saving it.
    """
    parser.description = long_description

    parser.add_argument(
        "--input", required=True, help="Specify the input file to normalize."
    )
    parser.add_argument(
        "--output",
        help=(
            "Specify the output file where the normalized content will be saved. "
            "If not provided, the input file will be overwritten."
        ),
        default=None,
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="If enabled, shows the normalized content without saving it.",
    )


def preview_content(content, file_extension):
    """
    Previews the normalized content in its original format.

    Args:
        content (dict or list): The normalized content to preview.
        file_extension (str): The file extension to determine the format (yaml, toml, json).
    """
    try:
        if file_extension == "yaml" or file_extension == "yml":
            print(yaml.safe_dump(content, default_flow_style=False))
        elif file_extension == "toml":
            print(toml.dumps(content))
        elif file_extension == "json":
            print(json.dumps(content, indent=4))
        else:
            logger.error(f"Unsupported file format for preview: {file_extension}")
    except Exception as e:
        logger.error(f"Error during preview: {e}")


def main(args):
    """
    Main function for the 'normalize' command.
    """
    # Vérification de l'existence du fichier d'entrée
    if not os.path.exists(args.input):
        logger.error(f"Input file {args.input} does not exist.")
        return

    try:
        # Utilisation du mécanisme de chargement
        content = load(args.input)
    except ValueError as e:
        logger.error(f"Error loading file: {e}")
        return

    # Application de la normalisation sur le contenu chargé
    normalized_content = normalize_content(content)

    # Détermination de l'extension du fichier pour la prévisualisation et la sauvegarde
    file_extension = args.input.split(".")[-1].lower()

    # Prévisualisation du contenu si demandé
    if args.preview:
        preview_content(normalized_content, file_extension)
    else:
        # Sauvegarde du fichier normalisé
        output_file = args.output if args.output else args.input
        try:
            save(output_file, normalized_content)
            logger.info(f"Normalized content saved to {output_file}.")
        except ValueError as e:
            logger.error(f"Error saving file: {e}")
