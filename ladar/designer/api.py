import inspect


def is_async_function(member):
    """Detect if a function or method is asynchronous."""
    return inspect.iscoroutinefunction(member) or inspect.isasyncgenfunction(member)


def extract_api_from_module(module, include_private=False):
    """Extract functions, classes, and signatures from a given module."""
    api_structure = {}

    def explore_members(members, parent_name="", visited=None):
        if visited is None:
            visited = set()

        for name, member in members:
            if not include_private and name.startswith("_"):
                continue

            full_name = f"{parent_name}.{name}" if parent_name else name

            # Avoid infinite recursion by checking if the member has already been visited
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
                sub_members = inspect.getmembers(member)
                explore_members(sub_members, parent_name=full_name, visited=visited)

    explore_members(inspect.getmembers(module))
    return api_structure


def analyze_stdlib(include_private=False):
    """Analyze the Python standard library and extract the API."""
    stdlib_api = {}

    # Use sys.stdlib_module_names for Python 3.10+, otherwise pkgutil.iter_modules
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
