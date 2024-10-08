.. ladar documentation master file, created by
   sphinx-quickstart on Thu Sep 26 15:49:01 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ladar documentation
===================

**Ladar is a tool designed to address a critical problem in software development:
managing API changes and automating the replacement of one library with another.**

Whether you're upgrading a library to a new version with breaking changes, **refactoring
your codebase, or migrating from one third-party library to another, Ladar simplifies
and automates the process**, reducing manual effort and **minimizing the risk of
errors**.

Additionally, **Ladar allows developers to create migration recipes, which can be shared
within the community to facilitate consistent and efficient transitions across
projects.**

The Problem
-----------

In software development, API (Application Programming Interface) changes are inevitable
as libraries and projects evolve. These changes can lead to breaking changes, version
mismatches, or the need to migrate between completely different libraries. Some of the
key challenges include:

- **Breaking changes**: Functions or methods are removed or altered, causing errors in
  code that depends on them.
- **Version incompatibilities**: Using different versions of the same library across
  projects can introduce incompatibilities.
- **Library migration**: When switching from one library to another, like migrating from
  `requests` to `httpx`, or like migrating from `eventlet` to `asyncio` the API
  differences must be handled efficiently.
- **Refactoring challenges**: Maintaining compatibility during internal code refactoring
  often requires careful manual changes.

Traditionally, handling these changes is a manual, error-prone, and time-consuming task,
requiring developers to manually inspect, refactor, and update codebases.

Ladar’s Solution
----------------

Ladar addresses these challenges by automating the extraction, comparison, and
substitution of API structures, making it possible to seamlessly transition between
different API versions or even entirely different libraries. This powerful tool
automates the process of refactoring code, ensuring that dependent code is updated
accordingly. Key functionalities include:

1. **API Extraction**:
   Ladar extracts the API structure (functions, methods, classes, and docstrings) from a
   Python module or project, generating a snapshot of the API for further analysis.

2. **API Comparison**:
   Using multiple algorithms, Ladar compares the API structures from different versions
   of a library or between entirely different libraries. This comparison reveals
   differences, similarities, and potential conflicts, helping you quickly identify
   areas where code needs to be updated.

3. **Mapping Generation**:
   After comparing APIs, Ladar generates a mapping that identifies equivalent API
   functions or methods between different versions or libraries. This mapping acts as a
   blueprint for how code dependent on one API can be transformed to use another.

4. **Automated Substitution**:
   Ladar’s most powerful feature is its ability to automatically substitute API calls
   in your project. Whether you're migrating from one library to another or simply
   upgrading to a new version, Ladar applies the generated mapping to your codebase,
   automating the necessary replacements and refactoring.

5. **Migration Recipes**:
   Ladar also allows developers to create **migration recipes**, which document the
   steps required to transition from one API version to another or to migrate between
   different libraries. These recipes can be shared with the wider developer community,
   enabling others to reuse them for similar transitions, fostering a collaborative
   environment for handling API changes.

Use Cases
---------

- **Version Upgrades**: When upgrading a third-party library with breaking changes,
  Ladar extracts the API from both the old and new versions, compares them, and
  automatically updates the codebase based on the changes.
- **Library Migration**: When migrating from one library to another (e.g., `requests` to
  `httpx`), Ladar automates the process of replacing old API calls with new ones,
  ensuring compatibility without the need for extensive manual refactoring.
- **Refactoring**: During internal codebase refactoring, Ladar ensures that API changes
  are properly applied throughout the project, reducing the likelihood of errors or
  regressions.
- **Community Collaboration**: Migration recipes generated by Ladar can be shared with
  the community, making it easier for other developers to perform similar migrations
  with minimal effort, enhancing consistency and speeding up adoption of best practices.

Conclusion
----------

By automating the extraction, comparison, and substitution of API structures, and
enabling the creation of shareable migration recipes, Ladar empowers developers to
efficiently manage API changes and seamlessly transition between libraries. This tool
significantly reduces the time and effort required for refactoring or library migration,
minimizes the risk of manual errors, and fosters collaboration within the community.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   manifesto.rst
   presentation.rst
   master-plan.rst
   extract.rst
   normalize.rst
   compare.rst
