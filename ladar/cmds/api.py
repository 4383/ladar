import importlib
import logging
import os

import ladar.common.venv as temp_env
from ladar.common.io import save
from ladar.common.package import install_local_dependencies, load_local_module
from ladar.common.ui import run_with_progress  # Import the progress wrapper
from ladar.designer.api import analyze_stdlib, extract_api_from_module

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "--module", help="Name of the module to analyze or path to a local module."
    )
    parser.add_argument(
        "--output", required=True, help="Output file (toml, yaml, json)"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private members in the analysis",
    )


def main(args):
    if args.module == "stdlib":
        api_structure = run_with_progress(
            analyze_stdlib,
            include_private=args.include_private,
            description="Analyzing stdlib",
            total_steps=50,
        )
    elif os.path.exists(args.module):
        temp_env.create_persistent_virtual_env()
        install_local_dependencies(os.path.dirname(args.module))
        try:
            module_name = load_local_module(args.module)
            module = importlib.import_module(module_name)
            api_structure = extract_api_from_module(
                module, include_private=args.include_private
            )
        except ImportError as e:
            logger.error(f"Error loading local module from {args.module}: {e}")
            return
    else:
        try:
            env_dir = temp_env.create_persistent_virtual_env()
            run_with_progress(
                temp_env.install_package_in_virtualenv,
                args.module,
                description=f"Installing {args.module}",
            )
            module = __import__(args.module)
            api_structure = extract_api_from_module(
                module, include_private=args.include_private
            )
        except ImportError as e:
            logger.error(f"Error importing module {args.module}: {e}")
            return

    try:
        save(args.output, api_structure)
        print(f"API saved to {args.output}")
    except ValueError as e:
        logger.error(f"Error saving file: {e}")
