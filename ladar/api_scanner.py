import argparse
import importlib.util
import json
import os
import pkgutil
import sys

import toml
import yaml

import ladar.common.venv as temp_env
from ladar.common.io import save
from ladar.designer.api import analyze_stdlib, extract_api_from_module


def load_local_module(module_path):
    """
    Load a local Python module from a given path.

    Args:
        module_path (str): The path to the local module or package.

    Returns:
        module: The imported Python module or None if the import fails.
    """
    module_name = os.path.splitext(os.path.basename(module_path))[0]

    if os.path.isdir(module_path):
        # If it's a directory, look for __init__.py to treat it as a package
        init_file = os.path.join(module_path, "__init__.py")
        if not os.path.exists(init_file):
            raise ImportError(f"No __init__.py found in directory {module_path}.")
        module_name = os.path.basename(module_path)
        spec = importlib.util.spec_from_file_location(module_name, init_file)
    else:
        # Load from a single Python file
        spec = importlib.util.spec_from_file_location(module_name, module_path)

    if spec is None:
        raise ImportError(f"Could not load module from path {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


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
        # Load a local module from a file or directory
        try:
            module = load_local_module(args.module)
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


if __name__ == "__main__":
    main()
