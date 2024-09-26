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
        "--version",
        help="Specify the version of the third-party module to install (e.g., '1.2.3')",
        default=None,
    )
    parser.add_argument(
        "--output", required=True, help="Output file (toml, yaml, json)"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private members in the analysis",
    )
    parser.add_argument(
        "--enable-legacy-compatibility",
        action="store_true",
        help="Enable legacy compatibility mode (install older setuptools/distutils for older packages).",
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
            # Create the virtual environment with the specified Python version (if provided)
            temp_env.create_persistent_virtual_env()

            # Ensure legacy compatibility is enabled if required
            ensure_legacy_compatibility_enabled(
                legacy_compatibility=args.enable_legacy_compatibility
            )

            # Handle versioning if specified
            if args.version:
                module_with_version = f"{args.module}=={args.version}"
            else:
                module_with_version = args.module

            # Install the specified module with the version (if any)
            run_with_progress(
                temp_env.install_package_in_virtualenv,
                module_with_version,
                description=f"Installing {module_with_version}",
            )

            # Import and extract API from the installed module
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
