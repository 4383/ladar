Normalize Command
=================

The ``normalize`` command is designed to process the content of a specified file by transforming names into lowercase, removing underscores, and flattening camel case. The command is useful for ensuring uniformity across file formats, making comparisons and analyses more reliable.

Command Overview
----------------

The ``normalize`` command performs the following operations:

1. **Lowercase conversion**: Converts all the names in the file to lowercase.
2. **Underscore removal**: Removes underscores from names.
3. **Camel case flattening**: Converts camel case names into lowercase with no separation.

You can specify an output file where the normalized content will be saved, or if no output file is provided, the input file will be overwritten. Additionally, you can preview the normalized content without saving it.

Options
-------

The following arguments are available for the ``normalize`` command:

.. autofunction:: ladar.cmds.normalize.add_arguments

Usage Examples
--------------

1. Normalize the content of a YAML file and overwrite the original file:

    .. code-block:: bash

        ladar normalize --input /path/to/input.yaml

2. Normalize the content of a TOML file and save the result to a different file:

    .. code-block:: bash

        ladar normalize --input /path/to/input.toml --output /path/to/output.toml

3. Preview the normalized content of a JSON file without saving it:

    .. code-block:: bash

        ladar normalize --input /path/to/input.json --preview

4. Normalize a YAML file and save the result in JSON format:

    .. code-block:: bash

        ladar normalize --input /path/to/input.yaml --output /path/to/output.json

Conclusion
----------

The ``normalize`` command provides an easy way to clean up and standardize the content of files, making it easier to perform comparisons or analyses. By using the preview option, you can see the results before making any changes to the original file.
