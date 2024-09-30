DBSCAN Algorithm
================

The DBSCAN algorithm is used to cluster similar API structures based on a density-based
approach. It can identify outliers and group similar structures together.

Parameters
----------

.. autofunction:: ladar.api.algorithms.dbscan..add_arguments

Usage Example
-------------

.. code-block:: bash

    ladar compare --structures /path/to/structure1.yaml /path/to/structure2.yaml --algorithms dbscan --dbscan-eps 0.3 --dbscan-min_samples 4 --output /path/to/output.yaml
