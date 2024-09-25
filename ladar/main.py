import argparse
import importlib
import pkgutil
import sys
from pathlib import Path


def discover_commands():
    # Recherche dynamique des sous-commandes dans le dossier 'cmds'
    commands = {}
    cmds_path = Path(__file__).parent / "cmds"
    for loader, module_name, is_pkg in pkgutil.iter_modules([str(cmds_path)]):
        module = importlib.import_module(f"ladar.cmds.{module_name}")
        if hasattr(module, "add_arguments") and hasattr(module, "main"):
            commands[module_name] = module
    return commands


def main():
    parser = argparse.ArgumentParser(
        prog="ladar", description="Ladar command-line tool"
    )

    # Découverte automatique des sous-commandes
    commands = discover_commands()

    # Ajout des sous-commandes dynamiquement
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    for command_name, module in commands.items():
        command_parser = subparsers.add_parser(
            command_name, help=f"{command_name} command"
        )
        module.add_arguments(command_parser)

    # Parse les arguments
    args = parser.parse_args()

    if args.command in commands:
        # Exécution dynamique de la sous-commande
        commands[args.command].main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
