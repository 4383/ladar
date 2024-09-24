import importlib.util
import logging
import os
import sys
from unittest import mock

import pytest

import ladar.common.venv as temp_env
from ladar.common.package import install_local_dependencies, load_local_module


# Mock logging to avoid output during testing
@pytest.fixture(autouse=True)
def mock_logging():
    with mock.patch.object(logging, "info") as mock_info, mock.patch.object(
        logging, "basicConfig"
    ):
        yield mock_info


def test_load_local_module_directory_with_pyproject_toml():
    # Setup
    module_path = "/path/to/module"
    with mock.patch("os.path.isdir", return_value=True), mock.patch(
        "os.path.exists", side_effect=lambda x: x.endswith("pyproject.toml")
    ):

        # Mock the temp_env method for installing the package
        with mock.patch.object(
            temp_env, "install_package_in_virtualenv"
        ) as mock_install:
            module_name = load_local_module(module_path)

            # Assertions
            assert module_name == os.path.basename(module_path)
            mock_install.assert_called_once_with(module_path)


def test_load_local_module_directory_without_init():
    # Setup
    module_path = "/path/to/module"
    with mock.patch("os.path.isdir", return_value=True), mock.patch(
        "os.path.exists", return_value=False
    ):

        with pytest.raises(ImportError, match="No __init__.py found"):
            load_local_module(module_path)


def test_load_local_module_single_python_file():
    # Setup
    module_path = "/path/to/module.py"
    module_name = os.path.splitext(os.path.basename(module_path))[0]

    with mock.patch("os.path.isdir", return_value=False), mock.patch(
        "importlib.util.spec_from_file_location"
    ) as mock_spec_loader, mock.patch(
        "importlib.util.module_from_spec"
    ) as mock_module_from_spec:

        mock_spec = mock.Mock()
        mock_spec_loader.return_value = mock_spec

        load_local_module(module_path)

        mock_spec_loader.assert_called_once_with(module_name, module_path)
        mock_module_from_spec.assert_called_once_with(mock_spec)
        mock_spec.loader.exec_module.assert_called_once()


def test_load_local_module_raises_import_error_on_invalid_spec():
    module_path = "/path/to/module.py"

    with mock.patch("os.path.isdir", return_value=False), mock.patch(
        "importlib.util.spec_from_file_location", return_value=None
    ):

        with pytest.raises(ImportError, match="Could not load module from path"):
            load_local_module(module_path)


def test_install_local_dependencies_requirements_txt():
    module_path = "/path/to/module"
    requirements_file = os.path.join(module_path, "requirements.txt")

    with mock.patch(
        "os.path.exists", side_effect=lambda x: x == requirements_file
    ), mock.patch.object(temp_env, "install_package_in_virtualenv") as mock_install:

        install_local_dependencies(module_path)

        mock_install.assert_called_once_with(f"-r {requirements_file}")


def test_install_local_dependencies_pyproject_toml():
    module_path = "/path/to/module"
    pyproject_file = os.path.join(module_path, "pyproject.toml")

    with mock.patch(
        "os.path.exists", side_effect=lambda x: x == pyproject_file
    ), mock.patch.object(temp_env, "install_package_in_virtualenv") as mock_install:

        install_local_dependencies(module_path)

        mock_install.assert_called_once_with(".")


def test_install_local_dependencies_no_dependency_files():
    module_path = "/path/to/module"

    with mock.patch("os.path.exists", return_value=False), mock.patch.object(
        temp_env, "install_package_in_virtualenv"
    ) as mock_install:

        install_local_dependencies(module_path)

        mock_install.assert_not_called()
