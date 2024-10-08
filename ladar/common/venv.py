import logging
import os
import shutil
import subprocess
import sys
import tempfile
import venv

from ladar.common.helpers import is_verbose

logger = logging.getLogger(__name__)

# Global variable to store the temporary virtual environment directory path
_temp_dir = None


def create_persistent_virtual_env():
    """
    Creates a persistent virtual environment in a temporary folder.

    This function creates a virtual environment using the `venv` module
    and stores its path in the global variable `_temp_dir`. If the virtual
    environment has already been created, it simply returns the path to it.

    Returns:
        str: The path to the virtual environment directory.

    Side Effects:
        - Adds the virtual environment's site-packages directory to `sys.path`
          to allow importing modules installed in the venv.

    Raises:
        RuntimeError: If the virtual environment creation fails.
    """
    global _temp_dir
    if _temp_dir is None:
        _temp_dir = tempfile.mkdtemp()  # Create a temporary directory for the venv
        venv.create(_temp_dir, with_pip=True)  # Create the virtual environment
        logger.info(f"Persistent virtual environment created in {_temp_dir}.")
        # Add the venv's site-packages to sys.path
        add_venv_to_syspath(_temp_dir)
    return _temp_dir


def add_venv_to_syspath(env_dir):
    """
    Adds the virtual environment's site-packages to `sys.path`.

    This function determines the path to the site-packages directory inside
    the virtual environment and inserts it at the beginning of `sys.path`,
    allowing modules installed in the virtual environment to be imported.

    Args:
        env_dir (str): The path to the virtual environment directory.

    Side Effects:
        - Modifies `sys.path` to prioritize packages installed in the virtual
          environment.

    Raises:
        RuntimeError: If the path to site-packages cannot be determined.
    """
    if os.name == "nt":
        # Windows case
        site_packages = os.path.join(env_dir, "Lib", "site-packages")
    else:
        # Linux/macOS case
        site_packages = os.path.join(
            env_dir,
            "lib",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages",
        )

    # Insert site-packages at the beginning of sys.path
    sys.path.insert(0, site_packages)
    logger.info(f"Added {site_packages} to sys.path")


def install_package_in_virtualenv(package):
    """
    Installs a package in the persistent virtual environment using `pip`.

    This function runs the `pip` command inside the virtual environment to install
    the specified package.

    The verbosity of the `pip` command is dynamically managed by the logging
    configuration.

    Args:
        package (str): The name of the package to install (e.g., 'requests').

    Raises:
        RuntimeError: If the virtual environment has not been created yet.
        subprocess.CalledProcessError: If the pip installation command fails.
    """
    global _temp_dir
    if _temp_dir is None:
        raise RuntimeError("The virtual environment has not been created yet.")

    # Determine the path to the Python executable inside the virtual environment
    if os.name != "nt":
        python_executable = os.path.join(_temp_dir, "bin", "python")
    else:
        python_executable = os.path.join(_temp_dir, "Scripts", "python.exe")

    try:
        # Run pip install command
        command = [python_executable, "-m", "pip", "install", package]

        if is_verbose("DEBUG"):
            # Show detailed pip logs if debug mode is enabled
            subprocess.check_call(command)
        else:
            # Capture the output if not in debug mode
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                logger.info(
                    f"{package} successfully installed in the virtual environment."
                )
            else:
                logger.error(f"Failed to install {package} in the virtual environment.")
                logger.error(stderr)
                raise subprocess.CalledProcessError(process.returncode, command)

    except subprocess.CalledProcessError:
        raise


def get_virtual_env_dir():
    """
    Returns the path to the persistent virtual environment directory.

    This function retrieves the path to the virtual environment if it exists.

    Returns:
        str: The path to the virtual environment directory.

    Raises:
        RuntimeError: If the virtual environment has not been created yet.
    """
    global _temp_dir
    if _temp_dir is None:
        raise RuntimeError("The virtual environment has not been created yet.")
    return _temp_dir


def clean_up():
    """
    Removes the persistent virtual environment directory.

    This function deletes the directory containing the virtual environment,
    cleaning up any temporary files created during the execution of the program.

    Side Effects:
        - Deletes the virtual environment directory from the filesystem.
    """
    global _temp_dir
    if _temp_dir is not None:
        shutil.rmtree(_temp_dir)  # Remove the directory
        logger.info(f"Persistent virtual environment removed: {_temp_dir}")
        _temp_dir = None
