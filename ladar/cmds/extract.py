import argparse
import importlib
import logging
import os
import sys
import textwrap

import ladar.common.venv as temp_env
from ladar.api.extract import analyze_stdlib, extract_api_from_module
from ladar.common.io import save
from ladar.common.package import install_local_dependencies, load_local_module
from ladar.common.ui import run_with_progress

logger = logging.getLogger(__name__)


command_description = """
Extract and save the API structure of a Python module, including standard library modules.
"""
long_description = """
The 'api' command analyzes the API of a specified Python module or a module from the
Python standard library (stdlib).

You can specify a third-party package, a local project, or a standard library module for analysis.
If 'stdlib' is passed as the module, the entire Python standard library will be analyzed.
Otherwise, you can analyze individual standard library modules (e.g., 'asyncio', 'http')
or third-party packages (e.g, 'requests', 'eventlet', 'flask').

The extracted API includes functions, classes, and other members, and is saved to a
specified output file (in TOML, YAML, or JSON format).

By default, only public members are included, but you can opt to include private members.
Additionally, for older modules that require legacy support, a compatibility mode is available.
"""


def add_arguments(parser):
    """
    Adds the argument options to the API command parser.

    Args:
        parser (argparse.ArgumentParser): The parser to which arguments are added.

    Arguments:
        --module (str):
            - Specify the module to analyze. The following types of values can be passed:
                1. A standard library module name (e.g., 'asyncio', 'http', 'pathlib')
                   to analyze a specific standard library module.
                2. 'stdlib' to analyze the entire Python standard library.
                3. The name of a third-party module, which will be installed in a virtual environment for analysis.
                4. The path to a local Python module or project.

        --version (str, optional):
            - Specify the version of a third-party module to install and analyze.
              Useful when specific versions are required for compatibility.

        --output (str, required):
            - Specify the output file where the extracted API will be saved.
              Supported formats are 'toml', 'yaml', and 'json'.

        --include-private (bool, optional):
            - Include private members (those starting with an underscore '_') in the API analysis.
              By default, only public members are included.

        --enable-legacy-compatibility (bool, optional):
            - Enable legacy compatibility mode to support older packages requiring older versions
              of setuptools or distutils for installation.
    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    parser.add_argument(
        "--module",
        help=(
            textwrap.dedent(
                """\
            Specify the module to analyze. The following types of values can be passed:
            1. A standard library module name (e.g., 'asyncio', 'http', 'pathlib'):
            This will analyze only the specified module from the Python standard library.
            2. 'stdlib': This will trigger the analysis of the entire Python standard library,
            extracting API details from all standard library modules.
            3. The name of a third-party module: The module will be automatically installed
            in a virtual environment, and its API will be analyzed. Optionally, you can specify
            the version of the module using the '--version' option.
            4. The path to a local Python project or module: This allows you to analyze a local
            Python project by providing its file path. The API structure of the local module will be extracted.
            Examples:
              --module asyncio          # Analyze the 'asyncio' module from the stdlib
              --module stdlib           # Analyze the entire standard library
              --module requests         # Analyze the 'requests' third-party module
              --module /path/to/module  # Analyze a local Python project"
        """
            )
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
            "Supported formats include 'toml', 'yaml', and 'json'. "
            "The file extension should match the desired format."
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
        help=textwrap.dedent(
            (
                """\
            Enable legacy compatibility mode for older packages that may require older versions of setuptools and distutils.
            When enabled, the necessary tools for legacy support will be installed in the virtual environment.
            This is useful for older packages that may not be compatible with modern versions of Python.
        """
            )
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
