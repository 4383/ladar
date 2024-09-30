.. _extract-cmd:

Extract Command
===============

The ``extract`` command is designed to extract and save the API structure of a Python
module, whether it belongs to the Python standard library, is a third-party package, or
is a local Python project. This command helps generate a snapshot of a module’s API,
including functions, classes, and other members, and saves the data in a specified
output file in formats such as TOML, YAML, or JSON.

Command Overview
----------------
The ``extract`` command can handle the following types of modules:

1. **Standard library modules**: Analyze any specific module from the Python standard
   library (e.g., ``asyncio``, ``http``).
2. **Entire Python standard library**: When the ``stdlib`` keyword is passed, it
   analyzes and extracts API details for all standard library modules.
3. **Third-party modules**: Analyze third-party Python packages. The command will
   automatically install the specified module in a virtual environment before performing
   the analysis.
4. **Local Python projects**: Provide the path to a local Python module or project to
   analyze its API structure.

By default, only public members of a module are included in the analysis, but you can
include private members using the ``--include-private`` option. Additionally, for older
modules that require legacy support, you can enable the legacy compatibility mode using
the ``--enable-legacy-compatibility`` option.

Options
-------

The following arguments are available for the `extract` command. They are derived
from the :func:`ladar.cmds.extract.add_arguments` which is the function which define the
command line arguments for this command:

.. autofunction:: ladar.cmds.extract.add_arguments

Usage Examples
--------------

1. Analyze the ``asyncio`` module from the standard library and save the API to a YAML file:

    .. code-block:: bash

        ladar extract --module asyncio --output /path/to/output.yaml

2. Analyze the entire Python standard library and save the API to a TOML file:

    .. code-block:: bash

        ladar extract --module stdlib --output /path/to/output.toml

3. Analyze a third-party module (e.g., ``requests``) and save the output as JSON:

    .. code-block:: bash

        ladar extract --module requests --output /path/to/output.json

4. Analyze a specific version of a third-party module (e.g., ``requests`` version 2.25.1):

    .. code-block:: bash

        ladar extract --module requests --version 2.25.1 --output /path/to/output.toml

5. Analyze a local Python project and save the output in TOML format:

    .. code-block:: bash

        ladar extract --module /path/to/local/project --output /path/to/output.toml

6. Analyze the ``http`` module from the standard library, including private members, and save the output in YAML format:

    .. code-block:: bash

        ladar extract --module http --include-private --output /path/to/output.yaml

7. Analyze an older third-party module with legacy compatibility mode enabled:

    .. code-block:: bash

        ladar extract --module some_old_package --enable-legacy-compatibility --output /path/to/output.yaml

8. Analyze the requests module, excluding docstrings, and save the output in JSON format:

    .. code-block:: bash

        ladar extract --module requests --exclude-docstrings --output /path/to/output.json


Conclusion
----------

The ``extract`` command provides a flexible way to analyze and document the API of
Python modules. Whether you are dealing with a module from the Python standard library,
a third-party package, or a local project, this command helps you generate an organized
view of the API and store it in a file format of your choice.
