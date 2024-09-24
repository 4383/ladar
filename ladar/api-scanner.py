import argparse
import inspect
import json
import os
import pkgutil
import sys

import toml
import yaml


def is_async_function(member):
    """Détecter si une fonction ou méthode est asynchrone."""
    return inspect.iscoroutinefunction(member) or inspect.isasyncgenfunction(member)


def extract_api_from_module(module, include_private=False):
    """Extraire les fonctions, classes et signatures d'un module donné."""
    api_structure = {}

    def explore_members(members, parent_name="", visited=None):
        if visited is None:
            visited = set()

        for name, member in members:
            if not include_private and name.startswith("_"):
                continue

            full_name = f"{parent_name}.{name}" if parent_name else name

            # Éviter la récursion infinie en vérifiant si le membre a déjà été visité
            if id(member) in visited:
                continue
            visited.add(id(member))

            if inspect.isfunction(member) or inspect.isbuiltin(member):
                try:
                    signature = str(inspect.signature(member))
                except (ValueError, TypeError):
                    signature = "N/A"  # Signature non disponible
                function_type = (
                    "async function" if is_async_function(member) else "function"
                )
                api_structure[full_name] = {
                    "type": function_type,
                    "signature": signature,
                }

            elif inspect.isclass(member):
                api_structure[full_name] = {"type": "class", "members": {}}
                # Explorer les méthodes des classes
                class_members = inspect.getmembers(member)
                for method_name, method in class_members:
                    if inspect.isfunction(method) or inspect.ismethod(method):
                        try:
                            signature = str(inspect.signature(method))
                        except (ValueError, TypeError):
                            signature = "N/A"  # Signature non disponible
                        method_type = (
                            "async method" if is_async_function(method) else "method"
                        )
                        api_structure[full_name]["members"][method_name] = {
                            "type": method_type,
                            "signature": signature,
                        }

            elif inspect.ismodule(member):
                api_structure[full_name] = {"type": "module", "members": {}}
                sub_members = inspect.getmembers(member)
                explore_members(sub_members, parent_name=full_name, visited=visited)

    explore_members(inspect.getmembers(module))
    return api_structure


def analyze_stdlib(include_private=False):
    """Analyser la bibliothèque standard Python et extraire l'API."""
    stdlib_api = {}

    # Utiliser sys.stdlib_module_names pour Python 3.10+, sinon pkgutil.iter_modules
    stdlib_modules = (
        sys.stdlib_module_names
        if hasattr(sys, "stdlib_module_names")
        else [name for _, name, _ in pkgutil.iter_modules()]
    )

    for module_name in stdlib_modules:
        try:
            module = __import__(module_name)
        except ImportError:
            continue

        stdlib_api[module_name] = extract_api_from_module(module, include_private)

    return stdlib_api


def save_output(api_structure, output_file, format_type):
    """Sauvegarder la structure API dans un fichier (TOML, YAML, JSON)."""
    with open(output_file, "w") as f:
        if format_type == "toml":
            toml.dump(api_structure, f)
        elif format_type == "yaml" or format_type == "yml":
            yaml.dump(api_structure, f, default_flow_style=False)
        elif format_type == "json":
            json.dump(api_structure, f, indent=4)
        else:
            raise ValueError(f"Format de fichier non supporté: {format_type}")


def main():
    parser = argparse.ArgumentParser(
        description="Extraire l'API d'une bibliothèque Python ou de la bibliothèque standard."
    )
    parser.add_argument(
        "--module",
        help="Nom du module à analyser, ou 'stdlib' pour analyser la bibliothèque standard",
    )
    parser.add_argument(
        "--output", required=True, help="Fichier de sortie (toml, yaml, json)"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Inclure les membres privés dans l'analyse",
    )

    args = parser.parse_args()

    # Déterminer le format de sortie
    output_ext = args.output.split(".")[-1].lower()

    if args.module == "stdlib":
        # Analyser la bibliothèque standard
        api_structure = analyze_stdlib(include_private=args.include_private)
    else:
        # Charger le module spécifié
        try:
            module = __import__(args.module)
            api_structure = extract_api_from_module(
                module, include_private=args.include_private
            )
        except ImportError as e:
            print(f"Erreur lors de l'importation du module {args.module}: {e}")
            return

    # Sauvegarder l'API dans le fichier spécifié
    try:
        save_output(api_structure, args.output, output_ext)
        print(f"API sauvegardée dans {args.output}")
    except ValueError as e:
        print(f"Erreur lors de la sauvegarde du fichier: {e}")


if __name__ == "__main__":
    main()
