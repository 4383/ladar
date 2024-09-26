import json
import xml.etree.ElementTree as ET
from io import StringIO
from unittest import mock
from unittest.mock import mock_open, patch

import pytest
import toml
import yaml

from ladar.common.io import (
    load,
    save_file,
    save_json,
    save_md,
    save_py,
    save_toml,
    save_txt,
    save_xml,
    save_yaml,
)

# Sample content for testing
yaml_content = """
name: John Doe
age: 30
"""
json_content = json.dumps({"name": "John Doe", "age": 30})
toml_content = toml.dumps({"name": "John Doe", "age": 30})


@pytest.mark.parametrize(
    "file_extension, file_content, expected_result",
    [
        # Test for YAML content
        ("yaml", yaml_content, {"name": "John Doe", "age": 30}),
        # Test for JSON content
        ("json", json_content, {"name": "John Doe", "age": 30}),
        # Test for TOML content
        ("toml", toml_content, {"name": "John Doe", "age": 30}),
    ],
)
def test_load_supported_formats(file_extension, file_content, expected_result):
    """
    Test the load function with supported file formats: YAML, TOML, and JSON.
    """
    file_path = f"test_file.{file_extension}"

    # Mock the open function to simulate file reading
    with mock.patch("builtins.open", mock.mock_open(read_data=file_content)):
        result = load(file_path)
        assert result == expected_result


def test_load_unsupported_format():
    """
    Test the load function with an unsupported file format.
    """
    file_path = "test_file.txt"

    with pytest.raises(ValueError, match="Unsupported file format"):
        load(file_path)


def test_load_parsing_error():
    """
    Test the load function when parsing fails (e.g., due to invalid syntax).
    """
    file_path = "test_file.yaml"

    # Simuler le contenu du fichier sans créer un fichier réel
    invalid_yaml_content = "name: John Doe\nage:"

    # Mock l'ouverture du fichier pour retourner un contenu invalide
    with mock.patch("builtins.open", mock.mock_open(read_data=invalid_yaml_content)):
        # Simuler une erreur de parsing YAML avec mock
        with mock.patch("yaml.safe_load", side_effect=yaml.YAMLError("Error parsing")):
            # S'assurer que l'erreur ValueError est levée
            with pytest.raises(ValueError, match="Error parsing"):
                load(file_path)


# Test the dispatch function for various file formats
@pytest.mark.parametrize(
    "filename,content,save_func",
    [
        ("test.txt", "Some text", save_txt),
        ("test.md", "Some markdown content", save_md),
        ("test.py", "print('Hello, World!')", save_py),
        ("test.toml", {"key": "value"}, save_toml),
        ("test.yaml", {"key": "value"}, save_yaml),
        ("test.json", {"key": "value"}, save_json),
        ("test.xml", ET.Element("root"), save_xml),
    ],
)
def test_save_file_dispatch(monkeypatch, filename, content, save_func):
    # Patch the save function to mock the actual file writing
    with patch(f"ladar.common.io.{save_func.__name__}") as mock_save:
        save_file(filename, content)
        mock_save.assert_called_once_with(filename, content)


# Test for unsupported file format
def test_save_file_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported file format: unknown"):
        save_file("test.unknown", "Some content")


# Test the save_txt function
def test_save_txt(monkeypatch):
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        save_txt("test.txt", "Some content")
        mock_file.assert_called_once_with("test.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("Some content")


# Test the save_toml function
def test_save_toml(monkeypatch):
    mock_file = mock_open()

    # Patch the built-in open function
    with patch("builtins.open", mock_file):
        # Patch the toml.dump function
        with patch("toml.dump") as mock_toml_dump:
            save_toml("test.toml", {"key": "value"})
            # Ensure the file is opened correctly
            mock_file.assert_called_once_with("test.toml", "w", encoding="utf-8")
            # Ensure toml.dump is called once with the correct arguments
            mock_toml_dump.assert_called_once_with({"key": "value"}, mock_file())


# Test the save_json function
def test_save_json(monkeypatch):
    mock_file = mock_open()

    # Patch the built-in open function
    with patch("builtins.open", mock_file):
        save_json("test.json", {"key": "value"})
        # Ensure the file is opened correctly
        mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")
        # Ensure the write method is called multiple times
        # (since json.dump writes in chunks)
        assert (
            mock_file().write.call_count > 1
        )  # json.dump typically writes in multiple steps
        # Aggregate the written content from the mock file writes
        written_content = "".join(call.args[0] for call in mock_file().write.mock_calls)
        # Verify that the written content matches the expected JSON output
        expected_content = json.dumps({"key": "value"}, indent=4)
        assert written_content == expected_content


# Test the save_xml function
def test_save_xml(monkeypatch):
    element = ET.Element("root")
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        with patch("xml.etree.ElementTree.ElementTree.write") as mock_write:
            save_xml("test.xml", element)
            mock_write.assert_called_once_with(
                "test.xml", encoding="utf-8", xml_declaration=True
            )


# Test the save_yaml function
def test_save_yaml(monkeypatch):
    mock_file = mock_open()

    # Mocking the open function
    with patch("builtins.open", mock_file):
        # Mocking yaml.dump function
        with patch("yaml.dump") as mock_yaml_dump:
            save_yaml("test.yaml", {"key": "value"})
            mock_file.assert_called_once_with("test.yaml", "w", encoding="utf-8")
            mock_yaml_dump.assert_called_once_with({"key": "value"}, mock_file())
