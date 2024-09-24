import json
import xml.etree.ElementTree as ET

import toml
import yaml


# Fonctions spécifiques à chaque type de fichier
def save_txt(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def save_md(filename, content):
    save_txt(filename, content)  # Même traitement que les fichiers txt


def save_py(filename, content):
    save_txt(filename, content)  # Même traitement que les fichiers txt


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


def save_rs(filename, content):
    save_txt(filename, content)  # Même traitement que les fichiers txt


def save_sql(filename, content):
    save_txt(filename, content)  # Même traitement que les fichiers txt


# Fonction de dispatch basée sur l'extension
def save_file(filename, content):
    extension = filename.split(".")[-1].lower()

    # Dictionnaire pour mapper l'extension à la fonction
    dispatch = {
        "txt": save_txt,
        "md": save_md,
        "py": save_py,
        "toml": save_toml,
        "yaml": save_yaml,
        "yml": save_yaml,  # Alias pour yaml
        "json": save_json,
        "xml": save_xml,
        "rs": save_rs,
        "sql": save_sql,
    }

    if extension in dispatch:
        # Appel de la fonction de sauvegarde appropriée
        dispatch[extension](filename, content)
    else:
        raise ValueError(f"Unsupported file format: {extension}")


# Exemple d'utilisation
if __name__ == "__main__":
    # Contenu à sauvegarder (peut être un texte ou un objet pour certains formats)
    content_txt = "Ceci est du texte"
    content_json = {"key": "value"}

    # Sauvegarder un fichier texte
    save_file("example.txt", content_txt)

    # Sauvegarder un fichier JSON
    save_file("example.json", content_json)

    # Sauvegarder un fichier YAML
    save_file("example.yaml", content_json)

    # Sauvegarder un fichier TOML
    save_file("example.toml", content_json)
