import ast
import json
import xml.etree.ElementTree as ET

import pytest
import toml
import yaml

from ladar.common.validate import (
    detect_and_validate,
    validate_json,
    validate_markdown,
    validate_python,
    validate_rst,
    validate_text,
    validate_toml,
    validate_xml,
    validate_yaml,
)


# Tests for validate_text
def test_validate_text_valid():
    assert validate_text("This is a valid text")


def test_validate_text_empty():
    with pytest.raises(ValueError, match="empty or invalid"):
        validate_text("")


def test_validate_text_not_string():
    with pytest.raises(ValueError, match="empty or invalid"):
        validate_text(123)


# Tests for validate_markdown
def test_validate_markdown_valid():
    assert validate_markdown("# Header")


def test_validate_markdown_invalid_syntax():
    with pytest.raises(ValueError, match="Minimally invalid Markdown"):
        validate_markdown("Invalid markdown text")


def test_validate_markdown_not_string():
    with pytest.raises(ValueError, match="Invalid Markdown"):
        validate_markdown(123)


# Tests for validate_python
def test_validate_python_valid():
    assert validate_python("a = 1")


def test_validate_python_invalid():
    with pytest.raises(ValueError, match="Invalid Python"):
        validate_python("a = ")


# Tests for validate_toml
def test_validate_toml_valid():
    assert validate_toml("key = 'value'")


def test_validate_toml_invalid():
    with pytest.raises(ValueError, match="Invalid TOML"):
        validate_toml("key: value")


# Tests for validate_yaml
def test_validate_yaml_valid():
    assert validate_yaml("key: value")


def test_validate_yaml_invalid():
    with pytest.raises(ValueError, match="Invalid YAML"):
        validate_yaml("{invalid: yaml,")


# Tests for validate_json
def test_validate_json_valid():
    assert validate_json('{"key": "value"}')


def test_validate_json_invalid():
    with pytest.raises(ValueError, match="Invalid JSON"):
        validate_json("{invalid: json}")


# Tests for validate_xml
def test_validate_xml_valid():
    assert validate_xml("<root><child/></root>")


def test_validate_xml_invalid():
    with pytest.raises(ValueError, match="Invalid XML"):
        validate_xml("<root><child></root>")


# Tests for validate_rst
def test_validate_rst_valid():
    assert validate_rst("=====\nTitle\n=====")


def test_validate_rst_invalid():
    with pytest.raises(ValueError, match="Invalid reStructuredText"):
        validate_rst("No RST syntax")


# Tests for detect_and_validate
def test_detect_and_validate_json():
    assert detect_and_validate('{"key": "value"}') is True


def test_detect_and_validate_yaml():
    assert detect_and_validate("key: value") is True


def test_detect_and_validate_toml():
    assert detect_and_validate("key = 'value'") is True


def test_detect_and_validate_xml():
    assert detect_and_validate("<root><child/></root>") is True


def test_detect_and_validate_python():
    assert detect_and_validate("a = 1") is True


def test_detect_and_validate_markdown():
    assert detect_and_validate("# Header") is True


def test_detect_and_validate_rst():
    assert detect_and_validate("=====\nTitle\n=====") is True


def test_detect_and_validate_text():
    assert detect_and_validate("Plain text") is True


def test_detect_and_validate_empty_content():
    with pytest.raises(ValueError, match="empty"):
        detect_and_validate("")
