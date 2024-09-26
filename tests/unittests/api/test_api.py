import inspect
import sys
import types
from unittest.mock import Mock, patch

import pytest

from ladar.api.api import analyze_stdlib, extract_api_from_module, is_async_function


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
    api = extract_api_from_module(mock_module, include_private=True)

    # Vérification des fonctions dans __class__ pour les méthodes de classe
    assert (
        "sync_func" in api["__class__"]["members"]
    ), "sync_func should be in the extracted API under __class__"
    assert (
        api["__class__"]["members"]["sync_func"]["type"] == "method"
    ), "sync_func should be identified as a method"

    assert (
        "async_func" in api["__class__"]["members"]
    ), "async_func should be in the extracted API under __class__"
    assert (
        api["__class__"]["members"]["async_func"]["type"] == "async method"
    ), "async_func should be identified as an async method"

    # Vérification de la NestedClass et des méthodes imbriquées
    assert "NestedClass" in api, "NestedClass should be in the extracted API"
    assert (
        api["NestedClass"]["type"] == "class"
    ), "NestedClass should be identified as a class"
    assert (
        "method" in api["NestedClass"]["members"]
    ), "method should be in NestedClass members"
    assert (
        api["NestedClass"]["members"]["method"]["type"] == "method"
    ), "method should be identified as a method"
    assert (
        api["NestedClass"]["members"]["async_method"]["type"] == "async method"
    ), "async_method should be identified as an async method"


def test_extract_api_from_module_exclude_private(mock_module):
    """Test that private members are excluded when include_private is False."""
    mock_module._private_func = lambda: None
    api = extract_api_from_module(mock_module, include_private=False)

    assert (
        "_private_func" not in api
    ), "Private functions should not be included when include_private is False"


def test_extract_api_from_module_include_private(mock_module):
    """Test that private members are included when include_private is True."""
    mock_module._private_func = lambda: None
    api = extract_api_from_module(mock_module, include_private=True)

    assert (
        "_private_func" in api
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
