import ast
import os


class AsyncChecker(ast.NodeVisitor):
    def __init__(self):
        self.has_async_function = False
        self.has_async_keywords = False

    def visit_AsyncFunctionDef(self, node):
        self.has_async_function = True
        self.generic_visit(node)  # Continue visiting children nodes

    def visit_Await(self, node):
        self.has_async_keywords = True
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.has_async_keywords = True
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.has_async_keywords = True
        self.generic_visit(node)


def check_for_async_in_code(code):
    tree = ast.parse(code)
    checker = AsyncChecker()
    checker.visit(tree)
    return checker.has_async_function, checker.has_async_keywords


def check_file_for_async(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    return check_for_async_in_code(code)


# Exemple d'utilisation :
file_path = "path_to_your_python_file.py"
async_function_present, async_keywords_present = check_file_for_async(file_path)

if async_function_present:
    if async_keywords_present:
        print(
            "Le fichier contient des fonctions async et des mots-clés async comme await, async for ou async with."
        )
    else:
        print(
            "Le fichier contient des fonctions async, mais il manque des mots-clés await, async for, async with."
        )
else:
    print("Le fichier ne contient aucune fonction async.")


def check_directory_for_async(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                async_function_present, async_keywords_present = check_file_for_async(
                    file_path
                )
                print(f"Fichier : {file_path}")
                if async_function_present:
                    if async_keywords_present:
                        print(
                            "  -> Contient des fonctions async et des mots-clés async."
                        )
                    else:
                        print(
                            "  -> Contient des fonctions async, mais pas de mots-clés async (await, async for, async with)."
                        )
                else:
                    print("  -> Aucune fonction async détectée.")


# Exemple d'utilisation sur un répertoire
directory_path = "path_to_your_directory"
check_directory_for_async(directory_path)
