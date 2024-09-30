.. _compare-cmd:

Compare Command
===============

The ``compare`` command is designed to compare multiple API structures that have been
previously extracted using the ``extract`` command. This command allows you to apply
one or more algorithms to compare API structures, helping to identify similarities,
differences, or specific patterns across multiple Python modules or projects. The
comparison results can be saved in formats such as TOML, YAML, or JSON.

Command Overview
----------------

The ``compare`` command handles comparison between two or more API structures and supports
various algorithms for performing the comparison. It can be used with both built-in algorithms
or third-party ones. Additionally, the user can pass specific parameters to control the behavior
of each algorithm.

By default, all available algorithms will be applied unless specified otherwise. You can
customize the behavior of each algorithm by passing algorithm-specific parameters.

Options
-------

The following arguments are available for the ``compare`` command. They are derived from
the :func:`ladar.cmds.compare.add_arguments`, which defines the command-line arguments for this command:

.. autofunction:: ladar.cmds.compare.add_arguments
   :no-index:

Additional Parameters
---------------------

Below is a list of additional parameters for each comparison algorithm. Each algorithm
may have specific options that can be passed through the command line when using the
``compare`` command. You can find details on these parameters by visiting the respective algorithm's documentation.

.. toctree::
   :maxdepth: 1
   :glob:

   algorithms/*

Usage Examples
--------------

1. Compare two API structures using the DBSCAN algorithm and save the result to a YAML file:

    .. code-block:: bash

        ladar compare --structures /path/to/structure1.yaml /path/to/structure2.yaml --algorithms dbscan --output /path/to/output.yaml

2. Compare three API structures using all available algorithms and save the result to a TOML file:

    .. code-block:: bash

        ladar compare --structures /path/to/structure1.yaml /path/to/structure2.yaml /path/to/structure3.yaml --output /path/to/output.toml

3. Compare two API structures using the DBSCAN algorithm with specific parameters (e.g., ``eps=0.3`` and ``min_samples=4``):

    .. code-block:: bash

        ladar compare --structures /path/to/structure1.yaml /path/to/structure2.yaml --algorithms dbscan --dbscan-eps 0.3 --dbscan-min_samples 4 --output /path/to/output.yaml

4. Compare two API structures using multiple algorithms (DBSCAN and TF-IDF) and save the result to a JSON file:

    .. code-block:: bash

        ladar compare --structures /path/to/structure1.yaml /path/to/structure2.yaml --algorithms dbscan tfidf --output /path/to/output.json

Conclusion
----------

The ``compare`` command provides a flexible and powerful way to compare API structures across
different Python modules and projects. By using customizable algorithms and supporting various
output formats, this command enables deep analysis and comparison of API data. Whether you want to
compare internal or third-party modules, ``compare`` helps you to better understand the relationships
between different APIs and structure the results in a clear, organized format.
