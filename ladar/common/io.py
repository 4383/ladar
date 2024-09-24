import json
import xml.etree.ElementTree as ET

import toml
import yaml


# Functions specific to each file type
def save_txt(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def save_md(filename, content):
    save_txt(filename, content)  # Same handling as txt files


def save_py(filename, content):
    save_txt(filename, content)  # Same handling as txt files


def save_toml(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        toml.dump(content, f)


def save_yaml(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(content, f)


def save_json(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)


def save_xml(filename, content):
    tree = ET.ElementTree(content)
    tree.write(filename, encoding="utf-8", xml_declaration=True)


# Dispatch function based on extension
def save_file(filename, content):
    extension = filename.split(".")[-1].lower()

    # Dictionary to map the extension to the function
    dispatch = {
        "txt": save_txt,
        "md": save_md,
        "py": save_py,
        "toml": save_toml,
        "yaml": save_yaml,
        "yml": save_yaml,  # Alias for yaml
        "json": save_json,
        "xml": save_xml,
    }

    if extension in dispatch:
        # Call the appropriate save function
        dispatch[extension](filename, content)
    else:
        raise ValueError(f"Unsupported file format: {extension}")
