import ast
import json
import re
import xml.etree.ElementTree as ET

import toml
import yaml


# Validation des différents formats
def validate_text(content):
    """Valide que le contenu est du texte brut valide (non vide)"""
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Le contenu texte est vide ou invalide.")
    return True


def validate_markdown(content):
    """Valide que le contenu est du markdown basique (syntaxe minimalement valide)"""
    if not isinstance(content, str):
        raise ValueError("Markdown invalide")
    # Vérification de quelques balises markdown courantes
    if not re.search(r"(^#+\s+|[*_]{1,2}.+[*_]{1,2})", content):
        raise ValueError("Markdown minimalement invalide")
    return True


def validate_python(content):
    """Valide que le contenu est un code Python syntaxiquement valide"""
    try:
        ast.parse(content)
    except SyntaxError as e:
        raise ValueError(f"Python invalide : {e}")
    return True


def validate_toml(content):
    """Valide que le contenu est un TOML valide"""
    try:
        toml.loads(content)
    except toml.TomlDecodeError as e:
        raise ValueError(f"TOML invalide : {e}")
    return True


def validate_yaml(content):
    """Valide que le contenu est un YAML valide"""
    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML invalide : {e}")
    return True


def validate_json(content):
    """Valide que le contenu est un JSON valide"""
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide : {e}")
    return True


def validate_xml(content):
    """Valide que le contenu est un XML valide"""
    try:
        ET.fromstring(content)
    except ET.ParseError as e:
        raise ValueError(f"XML invalide : {e}")
    return True


def validate_rust(content):
    """Valide que le contenu est un code Rust basiquement valide (fonction main présente)"""
    if "fn main()" not in content:
        raise ValueError("Rust invalide : fn main() non trouvé")
    return True


def validate_sql(content):
    """Valide que le contenu est une commande SQL basique (syntaxe de base)"""
    if not re.search(
        r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\s+", content, re.IGNORECASE
    ):
        raise ValueError("SQL invalide : commande SQL de base non trouvée")
    return True


def validate_rst(content):
    """Valide que le contenu est du reStructuredText basiquement valide"""
    if not re.search(r'^[=\-`:\'"~^_*+#<>]+$', content, re.MULTILINE):
        raise ValueError("reStructuredText invalide")
    return True


def validate_javascript(content):
    """Valide que le contenu est du JavaScript basiquement valide (syntaxe de base)"""
    if not re.search(r"\bfunction\b|\bvar\b|\bconst\b|\blet\b", content):
        raise ValueError("JavaScript invalide : éléments de base non trouvés")
    return True


# Dispatch des formats
def detect_and_validate(content):
    """Détecte le format et valide le contenu"""
    if isinstance(content, str):
        content = content.strip()

    if not content:
        raise ValueError("Le contenu est vide.")

    # Vérifier si le contenu est JSON
    try:
        json.loads(content)
        return validate_json(content)
    except json.JSONDecodeError:
        pass

    # Vérifier si le contenu est YAML
    try:
        yaml.safe_load(content)
        return validate_yaml(content)
    except yaml.YAMLError:
        pass

    # Vérifier si le contenu est TOML
    try:
        toml.loads(content)
        return validate_toml(content)
    except toml.TomlDecodeError:
        pass

    # Vérifier si le contenu est XML
    try:
        ET.fromstring(content)
        return validate_xml(content)
    except ET.ParseError:
        pass

    # Vérifier si le contenu est Python
    try:
        ast.parse(content)
        return validate_python(content)
    except SyntaxError:
        pass

    # Vérifier si le contenu est Markdown
    if re.search(r"(^#+\s+|[*_]{1,2}.+[*_]{1,2})", content):
        return validate_markdown(content)

    # Vérifier si le contenu est du Rust
    if "fn main()" in content:
        return validate_rust(content)

    # Vérifier si le contenu est du SQL
    if re.search(
        r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\s+", content, re.IGNORECASE
    ):
        return validate_sql(content)

    # Vérifier si le contenu est du reStructuredText
    if re.search(r'^[=\-`:\'"~^_*+#<>]+$', content, re.MULTILINE):
        return validate_rst(content)

    # Vérifier si le contenu est du JavaScript
    if re.search(r"\bfunction\b|\bvar\b|\bconst\b|\blet\b", content):
        return validate_javascript(content)

    # Si aucun format spécifique n'est détecté, on considère que c'est du texte brut
    return validate_text(content)


# Exemple d'utilisation
try:
    content = "# Markdown Example\n\nThis is a simple markdown."
    detect_and_validate(content)
    print("Contenu valide.")
except ValueError as e:
    print(e)
