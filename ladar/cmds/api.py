import argparse
import importlib
import logging
import os
import sys

import ladar.common.venv as temp_env
from ladar.common.io import save
from ladar.common.package import install_local_dependencies, load_local_module
from ladar.common.ui import run_with_progress
from ladar.designer.api import analyze_stdlib, extract_api_from_module

logger = logging.getLogger(__name__)


command_description = "Extract and save the API structure of a Python module."
long_descrption = """
The 'api' command is designed to analyze the API of a specified Python module,
whether it's a third-party package, a local project, or even the Python standard
library (stdlib).

It extracts the structure of the API, including functions, classes, and other members,
and saves this information in a specified output file (in TOML, YAML, or JSON format).

The command is useful for generating a snapshot of a module's API, whether for
documentation purposes, code auditing, or ensuring compatibility across versions.
By default, the command analyzes only public members, but you can include private
members if needed. Additionally, for older modules that require older versions of
setuptools or distutils, you can enable a legacy compatibility mode to handle such
dependencies.
"""


def add_arguments(parser):

    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_descrption

    parser.add_argument(
        "--module",
        help=(
            "Specify the name of the module to analyze or the path to a local module. "
            "If analyzing a third-party module, the module will be automatically installed "
            "in a virtual environment. If 'stdlib' is provided, the standard library will be analyzed."
        ),
    )
    parser.add_argument(
        "--version",
        help=(
            "Specify the version of the third-party module to install and analyze (e.g., '1.2.3'). "
            "This option is useful when specific versions of a module are required for compatibility reasons."
        ),
        default=None,
    )
    parser.add_argument(
        "--output",
        required=True,
        help=(
            "Specify the output file where the extracted API will be saved. "
            "Supported formats include 'toml', 'yaml', and 'json'. The file extension should match the desired format."
        ),
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help=(
            "Include private members in the API analysis. By default, private members "
            "(those starting with an underscore '_') are excluded from the extracted API structure."
        ),
    )
    parser.add_argument(
        "--enable-legacy-compatibility",
        action="store_true",
        help=(
            "Enable legacy compatibility mode for older packages that may require older versions of setuptools and distutils. "
            "When enabled, the necessary tools for legacy support will be installed in the virtual environment. "
            "This is useful for older packages that may not be compatible with modern versions of Python."
        ),
    )


def ensure_legacy_compatibility_enabled(legacy_compatibility=False):
    """
    Ensure that setuptools and distutils are installed in the virtual environment
    for older packages that may need them.

    Args:
        legacy_compatibility (bool): If True, enables the installation of older versions
                                     of setuptools and distutils for better retrocompatibility.
    """
    if not legacy_compatibility:
        logger.info(
            "Legacy compatibility mode is disabled. Skipping setuptools and distutils installation."
        )
        return

    try:
        import setuptools  # Check if setuptools is already installed

        logger.debug("Setuptools is already installed.")
    except ImportError:
        # Install an older version of setuptools that includes distutils
        logger.info("Installing an older version of setuptools with distutils support.")
        temp_env.install_package_in_virtualenv("setuptools==58.0.4")

    try:
        import distutils  # Check if distutils is available (for older packages)

        logger.debug("Distutils is already installed.")
    except ImportError:
        # Install a standalone version of distutils if needed
        logger.info("Installing distutils to support older packages.")
        temp_env.install_package_in_virtualenv("distlib")


def main(args):
    if args.module == "stdlib":
        logger.info("Analyzing the entire standard library (stdlib).")
        api_structure = run_with_progress(
            analyze_stdlib,
            include_private=args.include_private,
            description="Analyzing all standard library modules",
            total_steps=100,
        )
    else:
        try:
            if (
                args.module in sys.builtin_module_names
                or args.module in sys.stdlib_module_names
            ):
                logger.info(f"Analyzing stdlib module: {args.module}")
                module = __import__(args.module)
                api_structure = extract_api_from_module(
                    module, include_private=args.include_private
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
                temp_env.create_persistent_virtual_env()

                ensure_legacy_compatibility_enabled(
                    legacy_compatibility=args.enable_legacy_compatibility
                )

                if args.version:
                    module_with_version = f"{args.module}=={args.version}"
                else:
                    module_with_version = args.module

                run_with_progress(
                    temp_env.install_package_in_virtualenv,
                    module_with_version,
                    description=f"Installing {module_with_version}",
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
