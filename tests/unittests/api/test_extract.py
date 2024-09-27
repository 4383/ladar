import inspect
import sys
from unittest.mock import Mock, patch

import pytest

from ladar.api.extract import analyze_stdlib, extract_api_from_module, is_async_function


# Mock module for testing
class MockModule:
    def sync_func(self):
        """Synchronous function."""
        pass

    async def async_func(self):
        """Asynchronous function."""
        pass

    class NestedClass:
        def method(self):
            """Synchronous method."""
            pass

        async def async_method(self):
            """Asynchronous method."""
            pass

        def __init__(self, value):
            """Initialization method."""
            pass

        def __str__(self):
            """Magic method."""
            pass


@pytest.fixture
def mock_module():
    """Fixture to return a mock module with functions and classes."""
    return MockModule()


def test_is_async_function():
    """Test if the is_async_function correctly detects async functions."""

    def sync_func():
        pass

    async def async_func():
        pass

    assert not is_async_function(sync_func), "Sync function should return False"
    assert is_async_function(async_func), "Async function should return True"


def test_extract_api_from_module(mock_module):
    """Test if extract_api_from_module correctly extracts API information."""
    api = extract_api_from_module(
        mock_module, include_private=True, disable_normalization=True
    )

    # Vérifier que NestedClass existe bien dans MockModule
    assert "MockModule.NestedClass" in api, "NestedClass should be part of the API"

    # Vérification des méthodes dans NestedClass
    assert (
        "method" in api["MockModule.NestedClass"]["members"]
    ), "method should be in NestedClass members"
    assert (
        api["MockModule.NestedClass"]["members"]["method"]["type"] == "method"
    ), "method should be identified as a method"

    assert (
        "async_method" in api["MockModule.NestedClass"]["members"]
    ), "async_method should be in NestedClass members"
    assert (
        api["MockModule.NestedClass"]["members"]["async_method"]["type"]
        == "async method"
    ), "async_method should be identified as an async method"

    # Vérifier que __init__ est bien présent et que les méthodes magiques sont exclues
    assert (
        "__init__" in api["MockModule.NestedClass"]["members"]
    ), "__init__ should be included in the API"


def test_extract_api_from_module_include_private(mock_module):
    """Test that private members are included when include_private is True."""
    mock_module._private_func = lambda: None
    api = extract_api_from_module(
        mock_module,
        module_name="MockModule",
        include_private=True,
        disable_normalization=True,
    )

    # Verify that private function is included
    assert (
        "MockModule._private_func" in api
    ), "Private functions should be included when include_private is True"


def test_analyze_stdlib():
    """Test the analyze_stdlib function for basic functionality."""
    with patch("builtins.__import__", side_effect=lambda name: Mock()) as mock_import:
        api = analyze_stdlib(include_private=False)

        # Verify that standard library modules are being analyzed
        assert isinstance(
            api, dict
        ), "The result of analyze_stdlib should be a dictionary"
        mock_import.assert_called()

        # Check if some core modules were processed (mocked here)
        assert "sys" in api, "sys should be part of the standard library analysis"
        assert "os" in api, "os should be part of the standard library analysis"


def test_analyze_stdlib_module_import_error():
    """Test that modules that fail to import are skipped in analyze_stdlib."""
    # Patch the built-in import to simulate an ImportError for all modules
    with patch("builtins.__import__", side_effect=ImportError):
        api = analyze_stdlib(include_private=False)

        # Should return an empty dictionary if all imports fail
        assert api == {}, "The result should be an empty dictionary if all imports fail"


def test_extract_api_from_module_with_docstrings(mock_module):
    """Test that docstrings are included when include_docstrings is True."""
    api = extract_api_from_module(
        mock_module,
        include_private=True,
        include_docstrings=True,
        disable_normalization=True,
    )

    # Vérifier que NestedClass existe bien dans MockModule
    assert "MockModule.NestedClass" in api, "NestedClass should be part of the API"

    # Vérifier la docstring des méthodes dans NestedClass
    assert (
        api["MockModule.NestedClass"]["members"]["method"]["docstring"]
        == "Synchronous method."
    ), "method docstring should match 'Synchronous method.'"

    assert (
        api["MockModule.NestedClass"]["members"]["async_method"]["docstring"]
        == "Asynchronous method."
    ), "async_method docstring should match 'Asynchronous method.'"

    # Vérifier la docstring de __init__ dans NestedClass
    assert (
        api["MockModule.NestedClass"]["members"]["__init__"]["docstring"]
        == "Initialization method."
    ), "__init__ docstring should match 'Initialization method.'"


def test_extract_api_from_module_without_docstrings(mock_module):
    """Test that docstrings are not included when include_docstrings is False."""
    api = extract_api_from_module(
        mock_module,
        include_private=True,
        include_docstrings=False,
        disable_normalization=True,
    )

    # Vérification que NestedClass existe bien dans MockModule
    assert "MockModule.NestedClass" in api, "NestedClass should be part of the API"

    # Vérifier que 'method' et 'async_method' sont bien dans NestedClass
    assert (
        "method" in api["MockModule.NestedClass"]["members"]
    ), "method should be in NestedClass members"
    assert (
        "async_method" in api["MockModule.NestedClass"]["members"]
    ), "async_method should be in NestedClass members"

    # Vérification que les docstrings ne sont pas incluses
    assert (
        "docstring" not in api["MockModule.NestedClass"]["members"]["method"]
    ), "The docstring for method should not be included"
    assert (
        "docstring" not in api["MockModule.NestedClass"]["members"]["async_method"]
    ), "The docstring for async_method should not be included"


def test_extract_api_from_module_with_normalization(mock_module):
    """
    Test that API structure is normalized by default.

    The function verifies that:
    - Class and method names are normalized (lowercase, without underscores).
    - Docstrings are only converted to lowercase, without removing spaces or other characters.

    Args:
        mock_module (MockModule): The mock module for testing purposes.
    """
    api = extract_api_from_module(
        mock_module, include_private=True, include_docstrings=True
    )

    # Check that class names are normalized
    assert (
        "mockmodule.nestedclass" in api
    ), "NestedClass should be normalized in the API"

    # Check that method names are normalized
    assert (
        "method" in api["mockmodule.nestedclass"]["members"]
    ), "method should be normalized in NestedClass members"

    # Ensure async_method is normalized and present (without underscore, due to normalization)
    assert (
        "asyncmethod" in api["mockmodule.nestedclass"]["members"]
    ), "asyncmethod should be present and normalized in NestedClass members"

    # Check that docstrings are only converted to lowercase
    assert (
        api["mockmodule.nestedclass"]["members"]["method"]["docstring"]
        == "synchronous method."
    ), "Docstring should be converted to lowercase"

    # Check docstring for asyncmethod
    assert (
        api["mockmodule.nestedclass"]["members"]["asyncmethod"]["docstring"]
        == "asynchronous method."
    ), "Async method docstring should be converted to lowercase"


def test_extract_api_from_module_without_normalization(mock_module):
    """
    Test that API structure is not normalized when disable_normalization is True.

    The function verifies that:
    - Class and method names are not normalized.
    - Docstrings are not modified in any way when normalization is disabled.

    Args:
        mock_module (MockModule): The mock module for testing purposes.
    """
    api = extract_api_from_module(
        mock_module,
        include_private=True,
        include_docstrings=True,
        disable_normalization=True,
    )

    # Check that class names are not normalized
    assert "MockModule.NestedClass" in api, "NestedClass should not be normalized"

    # Check that method names are not normalized
    assert (
        "method" in api["MockModule.NestedClass"]["members"]
    ), "method should not be normalized in NestedClass members"

    # Check that docstrings are not converted to lowercase
    assert (
        api["MockModule.NestedClass"]["members"]["method"]["docstring"]
        == "Synchronous method."
    ), "Docstring should not be converted to lowercase"

    assert (
        api["MockModule.NestedClass"]["members"]["async_method"]["docstring"]
        == "Asynchronous method."
    ), "Async method docstring should not be converted to lowercase"
