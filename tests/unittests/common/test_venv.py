import os
import shutil
import sys

import pytest

import ladar.common.venv as temp_env


# Fixture to clean up the environment after each test
@pytest.fixture(autouse=True)
def clean_up_env():
    yield
    temp_env.clean_up()


def test_create_persistent_virtual_env():
    """
    Test if the virtual environment is created successfully and the directory exists.
    """
    env_dir = temp_env.create_persistent_virtual_env()
    assert os.path.exists(env_dir), "The virtual environment directory should exist."
    assert os.path.isdir(env_dir), "The environment should be a directory."


def test_install_package_in_virtualenv():
    """
    Test if a package can be successfully installed in the virtual environment.
    """
    env_dir = temp_env.create_persistent_virtual_env()

    # Install a package (e.g., requests)
    temp_env.install_package_in_virtualenv("requests")

    # Check if the installed package is present in the site-packages directory
    site_packages = (
        os.path.join(
            env_dir,
            "lib",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages",
        )
        if os.name != "nt"
        else os.path.join(env_dir, "Lib", "site-packages")
    )

    installed_packages = os.listdir(site_packages)
    assert "requests" in [
        pkg for pkg in installed_packages if "requests" in pkg
    ], "requests should be installed in the virtual environment."


def test_get_virtual_env_dir():
    """
    Test if the correct virtual environment directory is returned.
    """
    env_dir = temp_env.create_persistent_virtual_env()
    retrieved_env_dir = temp_env.get_virtual_env_dir()

    assert (
        env_dir == retrieved_env_dir
    ), "The retrieved environment directory should match the created one."


def test_clean_up():
    """
    Test if the virtual environment is removed successfully after cleanup.
    """
    env_dir = temp_env.create_persistent_virtual_env()
    assert os.path.exists(
        env_dir
    ), "The environment directory should exist before cleanup."

    # Clean up the environment
    temp_env.clean_up()

    assert not os.path.exists(
        env_dir
    ), "The environment directory should be deleted after cleanup."


def test_error_when_no_env_created():
    """
    Test if an error is raised when trying to install a package without creating a
    virtual environment.
    """
    temp_env.clean_up()  # Ensure no environment exists

    with pytest.raises(
        RuntimeError, match="The virtual environment has not been created yet."
    ):
        temp_env.install_package_in_virtualenv("requests")
