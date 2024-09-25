import importlib.util
import logging
import os
import sys

import ladar.common.venv as temp_env

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_local_module(module_path):
    """
    Load a local Python module or project from a given path.

    Args:
        module_path (str): The path to the local module or package.

    Returns:
        str: The name of the module (to be imported later) or None if the import fails.
    """
    module_name = os.path.splitext(os.path.basename(module_path))[0]

    # Check if the directory contains pyproject.toml, setup.py, or setup.cfg
    if os.path.isdir(module_path) and any(
        os.path.exists(os.path.join(module_path, f))
        for f in ["pyproject.toml", "setup.py", "setup.cfg"]
    ):
        # Treat as a project root and install the package without requiring __init__.py
        logger.debug(
            f"Detected Python project at {module_path}. Installing it as a package."
        )
        temp_env.install_package_in_virtualenv(module_path)
        # Return the module name to be imported later
        return module_name

    # If it's a directory but not a recognized project root, check for __init__.py
    elif os.path.isdir(module_path):
        init_file = os.path.join(module_path, "__init__.py")
        if not os.path.exists(init_file):
            raise ImportError(f"No __init__.py found in directory {module_path}.")
        spec = importlib.util.spec_from_file_location(module_name, init_file)

    else:
        # Load from a single Python file
        spec = importlib.util.spec_from_file_location(module_name, module_path)

    if spec is None:
        raise ImportError(f"Could not load module from path {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module_name


def install_local_dependencies(module_path):
    """
    Install dependencies from a local module's requirements.txt or pyproject.toml.

    Args:
        module_path (str): The path to the local module or package.

    Raises:
        RuntimeError: If the virtual environment has not been created yet.
    """
    requirements_file = os.path.join(module_path, "requirements.txt")
    pyproject_file = os.path.join(module_path, "pyproject.toml")

    # Install dependencies from requirements.txt if it exists
    if os.path.exists(requirements_file):
        logger.debug(f"Installing dependencies from {requirements_file}.")
        temp_env.install_package_in_virtualenv(f"-r {requirements_file}")
    # Install dependencies from pyproject.toml if it exists
    elif os.path.exists(pyproject_file):
        logger.debug(f"Installing dependencies from {pyproject_file}.")
        temp_env.install_package_in_virtualenv(".")  # Install the whole package
    else:
        logger.debug("No dependency file found (requirements.txt or pyproject.toml).")
