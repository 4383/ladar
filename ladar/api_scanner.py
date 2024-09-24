import argparse
import importlib.util
import json
import logging
import os
import sys

import toml
import yaml

import ladar.common.venv as temp_env
from ladar.common.io import save
from ladar.common.package import install_local_dependencies, load_local_module
from ladar.designer.api import analyze_stdlib, extract_api_from_module

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Extract the API from a Python library or the standard library."
    )
    parser.add_argument(
        "--module",
        help="Name of the module to analyze, 'stdlib' to analyze the standard library, "
        "or the path to a local module (directory or Python file).",
    )
    parser.add_argument(
        "--output", required=True, help="Output file (toml, yaml, json)"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private members in the analysis",
    )

    args = parser.parse_args()

    if args.module == "stdlib":
        # Analyze the standard library
        api_structure = analyze_stdlib(include_private=args.include_private)
    elif os.path.exists(args.module):
        # Create a virtual environment and install local module dependencies
        temp_env.create_persistent_virtual_env()
        install_local_dependencies(os.path.dirname(args.module))

        # Load the local module or project
        try:
            module_name = load_local_module(args.module)
            module = importlib.import_module(module_name)
            api_structure = extract_api_from_module(
                module, include_private=args.include_private
            )
        except ImportError as e:
            print(f"Error loading local module from {args.module}: {e}")
            return
    else:
        # Load the specified module from installed packages
        try:
            env_dir = temp_env.create_persistent_virtual_env()
            temp_env.install_package_in_virtualenv(args.module)
            module = __import__(args.module)
            api_structure = extract_api_from_module(
                module, include_private=args.include_private
            )
        except ImportError as e:
            print(f"Error importing module {args.module}: {e}")
            return

    # Save the API to the specified file
    try:
        save(args.output, api_structure)
        print(f"API saved to {args.output}")
    except ValueError as e:
        print(f"Error saving file: {e}")
