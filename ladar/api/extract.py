import importlib
import inspect
import json
import pkgutil
import sys
from datetime import datetime

from ladar.api.normalize import normalize_docstring, normalize_value


def extract_module_info(module_name):
    try:
        module = importlib.import_module(module_name)

        version = getattr(module, "__version__", None)

        if version is None or module_name == "stdlib":
            if (
                module_name in sys.builtin_module_names
                or module.__name__ in sys.modules
                or module_name == "stdlib"
            ):
                version = f"Python stdlib - Python {sys.version}"
            else:
                version = "unknown"

        module_info = {
            "ladar": {
                "module_name": module_name,
                "module_version": version,
                "date": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            }
        }

        return module_info

    except ModuleNotFoundError:
        print(f"Module {module_name} non trouvé.")
        return None


# Exemple d'utilisation
module_info = extract_module_info("os")  # Un module de la stdlib


def is_async_function(member):
    """
    Detect if a given function or method is asynchronous.

    Args:
        member (object): A function, method, or other callable object.

    Returns:
        bool: True if the function is asynchronous (either coroutine or async generator), False otherwise.
    """
    return inspect.iscoroutinefunction(member) or inspect.isasyncgenfunction(member)


def should_include_member(name):
    """
    Determine if a member should be included in the API extraction based on its name.

    Args:
        name (str): The name of the member.

    Returns:
        bool: True if the member should be included, False otherwise.
    """
    # Exclude built-in methods and magic methods (those with double underscores),
    # except for __init__ which is important for class initialization.
    if name == "__init__":
        return True
    return not (name.startswith("__") and name.endswith("__"))


def extract_api_from_module(
    module,
    module_name=None,
    include_private=False,
    include_docstrings=True,
    disable_normalization=False,
):
    """
    Extract functions, classes, their signatures, and optionally docstrings from a given module.
    Apply normalization unless disabled by the user.

    Args:
        module (module or class): The Python module or object to analyze.
        module_name (str): A default name to use if the module has no __name__ attribute.
        include_private (bool): Whether to include private functions and members (those starting with "_").
        include_docstrings (bool): Whether to include docstrings in the extracted API.
        disable_normalization (bool): If True, normalization will be disabled.

    Returns:
        dict: A dictionary representing the structure of the module's API.
    """
    api_structure = {}

    def explore_members(members, parent_name="", visited=None):
        if visited is None:
            visited = set()

        for name, member in members:
            # Skip private members unless included
            if not include_private and name.startswith("_"):
                continue

            # Ensure the __init__ method is included but skip other magic methods
            if not should_include_member(name):
                continue

            full_name = f"{parent_name}.{name}" if parent_name else name

            if id(member) in visited:
                continue
            visited.add(id(member))

            docstring = inspect.getdoc(member) if include_docstrings else None
            # Apply normalization if enabled
            if not disable_normalization:
                full_name = normalize_value(full_name)
                if docstring:
                    docstring = normalize_docstring(docstring)

            if inspect.isfunction(member) or inspect.isbuiltin(member):
                try:
                    signature = str(inspect.signature(member))
                    if not disable_normalization:
                        signature = normalize_value(signature)
                except (ValueError, TypeError):
                    signature = None

                function_type = (
                    "async function" if is_async_function(member) else "function"
                )
                api_structure[full_name] = {
                    "type": function_type,
                }
                if signature:
                    api_structure[full_name]["signature"] = signature
                if docstring:
                    api_structure[full_name]["docstring"] = docstring

            elif inspect.isclass(member):
                api_structure[full_name] = {"type": "class", "members": {}}
                if docstring:
                    api_structure[full_name]["docstring"] = docstring

                class_members = inspect.getmembers(member)
                for method_name, method in class_members:
                    if not should_include_member(method_name):
                        continue

                    if inspect.isfunction(method) or inspect.ismethod(method):
                        try:
                            signature = str(inspect.signature(method))
                        except (ValueError, TypeError):
                            signature = None

                        method_type = (
                            "async method" if is_async_function(method) else "method"
                        )
                        normalized_method_name = (
                            normalize_value(method_name)
                            if not disable_normalization
                            else method_name
                        )
                        api_structure[full_name]["members"][normalized_method_name] = {
                            "type": method_type,
                        }
                        if signature:
                            api_structure[full_name]["members"][normalized_method_name][
                                "signature"
                            ] = signature
                        method_docstring = (
                            inspect.getdoc(method) if include_docstrings else None
                        )
                        if method_docstring and not disable_normalization:
                            method_docstring = normalize_docstring(method_docstring)

                        if method_docstring:
                            api_structure[full_name]["members"][normalized_method_name][
                                "docstring"
                            ] = method_docstring

            elif inspect.ismodule(member):
                api_structure[full_name] = {"type": "module", "members": {}}
                if docstring:
                    api_structure[full_name]["docstring"] = docstring

                sub_members = inspect.getmembers(member)
                explore_members(sub_members, parent_name=full_name, visited=visited)

    # Use the module's name if available, otherwise, use the provided module_name or a default name
    if module_name is None:
        module_name = getattr(module, "__name__", module.__class__.__name__)

    explore_members(inspect.getmembers(module), parent_name=module_name)
    return api_structure


def analyze_stdlib(include_private=False):
    """
    Analyze the Python standard library and extract its API structure.

    Args:
        include_private (bool): Whether to include private members in the API extraction.

    Returns:
        dict: A dictionary where keys are standard library module names, and values are the
        extracted API structures of those modules.
    """
    stdlib_api = {}

    # Get the list of standard library modules for Python 3.10+ or use pkgutil for older versions
    stdlib_modules = (
        sys.stdlib_module_names
        if hasattr(sys, "stdlib_module_names")
        else [name for _, name, _ in pkgutil.iter_modules()]
    )

    # Loop through each standard library module and extract its API
    for module_name in stdlib_modules:
        try:
            module = __import__(module_name)
        except ImportError:
            continue  # Skip modules that fail to import

        stdlib_api[module_name] = extract_api_from_module(module, include_private)

    return stdlib_api
