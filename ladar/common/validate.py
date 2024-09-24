import ast
import json
import re
import xml.etree.ElementTree as ET

import toml
import yaml


# Validation of different formats
def validate_text(content):
    """Validates that the content is valid plain text (non-empty)"""
    if not isinstance(content, str) or not content.strip():
        raise ValueError("The text content is empty or invalid.")
    return True


def validate_markdown(content):
    """Validates that the content is basic markdown (minimally valid syntax)"""
    if not isinstance(content, str):
        raise ValueError("Invalid Markdown")
    # Check for some common markdown tags
    if not re.search(r"(^#+\s+|[*_]{1,2}.+[*_]{1,2})", content):
        raise ValueError("Minimally invalid Markdown")
    return True


def validate_python(content):
    """Validates that the content is syntactically valid Python code"""
    try:
        ast.parse(content)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python: {e}")
    return True


def validate_toml(content):
    """Validates that the content is valid TOML"""
    try:
        toml.loads(content)
    except toml.TomlDecodeError as e:
        raise ValueError(f"Invalid TOML: {e}")
    return True


def validate_yaml(content):
    """Validates that the content is valid YAML"""
    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")
    return True


def validate_json(content):
    """Validates that the content is valid JSON"""
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    return True


def validate_xml(content):
    """Validates that the content is valid XML"""
    try:
        ET.fromstring(content)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}")
    return True


def validate_rst(content):
    """Validates that the content is basic valid reStructuredText"""
    if not re.search(r'^[=\-`:\'"~^_*+#<>]+$', content, re.MULTILINE):
        raise ValueError("Invalid reStructuredText")
    return True


# Format dispatch
def detect_and_validate(content):
    """Detects the format and validates the content"""
    if isinstance(content, str):
        content = content.strip()

    if not content:
        raise ValueError("The content is empty.")

    # Check if the content is JSON
    try:
        json.loads(content)
        return validate_json(content)
    except json.JSONDecodeError:
        pass

    # Check if the content is YAML
    try:
        yaml.safe_load(content)
        return validate_yaml(content)
    except yaml.YAMLError:
        pass

    # Check if the content is TOML
    try:
        toml.loads(content)
        return validate_toml(content)
    except toml.TomlDecodeError:
        pass

    # Check if the content is XML
    try:
        ET.fromstring(content)
        return validate_xml(content)
    except ET.ParseError:
        pass

    # Check if the content is Python
    try:
        ast.parse(content)
        return validate_python(content)
    except SyntaxError:
        pass

    # Check if the content is Markdown
    if re.search(r"(^#+\s+|[*_]{1,2}.+[*_]{1,2})", content):
        return validate_markdown(content)

    # Check if the content is reStructuredText
    if re.search(r'^[=\-`:\'"~^_*+#<>]+$', content, re.MULTILINE):
        return validate_rst(content)

    # If no specific format is detected, consider it plain text
    return validate_text(content)
