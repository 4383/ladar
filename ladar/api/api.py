import inspect
import pkgutil
import sys


def is_async_function(member):
    """
    Detect if a given function or method is asynchronous.

    Args:
        member (object): A function, method, or other callable object.

    Returns:
        bool: True if the function is asynchronous (either coroutine or async generator), False otherwise.
    """
    return inspect.iscoroutinefunction(member) or inspect.isasyncgenfunction(member)


def extract_api_from_module(module, include_private=False):
    """
    Extract functions, classes, and their signatures from a given module.

    Args:
        module (module): The Python module to analyze.
        include_private (bool): Whether to include private functions and members (those starting with "_").

    Returns:
        dict: A dictionary representing the structure of the module's API. Keys are the names of
        functions, classes, and submodules, with their types and signatures as values.
    """
    api_structure = {}

    def explore_members(members, parent_name="", visited=None):
        """
        Recursively explore module members, extracting their API information.

        Args:
            members (list): List of members (name, object) pairs.
            parent_name (str): The hierarchical name of the parent member.
            visited (set): A set of visited members to avoid infinite recursion.
        """
        if visited is None:
            visited = set()

        for name, member in members:
            # Skip private members unless included
            if not include_private and name.startswith("_"):
                continue

            full_name = f"{parent_name}.{name}" if parent_name else name

            # Prevent infinite loops by checking if the member has already been visited
            if id(member) in visited:
                continue
            visited.add(id(member))

            if inspect.isfunction(member) or inspect.isbuiltin(member):
                try:
                    signature = str(inspect.signature(member))
                except (ValueError, TypeError):
                    signature = "N/A"  # Signature not available
                function_type = (
                    "async function" if is_async_function(member) else "function"
                )
                api_structure[full_name] = {
                    "type": function_type,
                    "signature": signature,
                }

            elif inspect.isclass(member):
                api_structure[full_name] = {"type": "class", "members": {}}
                # Explore class methods
                class_members = inspect.getmembers(member)
                for method_name, method in class_members:
                    if inspect.isfunction(method) or inspect.ismethod(method):
                        try:
                            signature = str(inspect.signature(method))
                        except (ValueError, TypeError):
                            signature = "N/A"  # Signature not available
                        method_type = (
                            "async method" if is_async_function(method) else "method"
                        )
                        api_structure[full_name]["members"][method_name] = {
                            "type": method_type,
                            "signature": signature,
                        }

            elif inspect.ismodule(member):
                api_structure[full_name] = {"type": "module", "members": {}}
                # Explore submodule members recursively
                sub_members = inspect.getmembers(member)
                explore_members(sub_members, parent_name=full_name, visited=visited)

    # Start the member exploration
    explore_members(inspect.getmembers(module))
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
