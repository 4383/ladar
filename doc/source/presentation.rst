Ladar Overview
==============

Ladar is a powerful tool for extracting, comparing, and substituting API structures in
Python projects. This page presents four different types of diagrams to illustrate
various aspects of Ladar: the overall process, interaction between components, usage
sequence, and the data processing pipeline.

Flowchart Diagram
-----------------

This flowchart provides a detailed view of the core functionality of Ladar. It explains
how Ladar processes API structures, from extraction to substitution, highlighting the
interaction between various components and the overall workflow.

1. **Extractor**:
   - The process begins with the :ref:`extract`.
   - Ladar takes a Python module, analyzes it, and extracts its API structure
     (functions, classes, methods, and optionally docstrings).
   - The extracted API structure is stored in a specified file (in TOML, YAML, or JSON
     format) for further analysis.

2. **Comparator**:
   - After the extraction phase, the :ref:`compare` command is used to compare two or
     more API structures.
   - The comparison is performed using one or more algorithms (e.g., DBSCAN, TF-IDF,
     etc.), which analyze the similarities and differences between the structures.
   - The result of the comparison is a detailed mapping of changes or similarities
     between the API structures, which is then saved.

3. **Mapping Generator**:
   - Once the API structures have been compared, Ladar generates a substitution mapping.
   - This mapping serves as a blueprint for how parts of the code in one module (or
     project) can be substituted by equivalent parts from another module, based on the
     comparison results.

4. **Substitutor**:
   - Finally, the `substitute` command applies the generated mapping to a given project.
   - The mapping identifies and replaces API calls, functions, or methods from one
     module with their equivalents from another, facilitating automatic code
     transformation.

.. graphviz::

   digraph G {
      "User" -> "Extractor" [label="extract API"];
      "Extractor" -> "Storage" [label="save API structure"];
      "User" -> "Comparator" [label="compare structures"];
      "Comparator" -> "Algorithms" [label="run algorithms"];
      "Algorithms" -> "Mapping Generator" [label="generate mapping"];
      "User" -> "Substitutor" [label="apply mapping to project"];
   }

**Key Details**:
- **API Extraction**: The process starts by extracting the structure of a module, saving
  it in a structured format for later comparison.
- **API Comparison**: Multiple API structures can be compared using customizable
  algorithms, producing insights about their differences or similarities.
- **Mapping Generation**: A mapping between similar elements of the API structures is
  generated, ready for substitution.
- **Code Substitution**: The substitution phase applies the generated mapping to a
  project, automating the code transformation process.

This flowchart encapsulates the entire lifecycle of Ladar, demonstrating how API
structures are processed and manipulated from extraction to substitution, providing a
powerful mechanism for code comparison and transformation.

UML Sequence Diagram
---------------------

This sequence diagram illustrates the interaction between the user, the Ladar commands
(like `extract`, `compare`, and `substitute`), and the internal components.

.. plantuml::

   @startuml
   User -> Ladar: extract API
   Ladar -> Extractor: analyze module
   Extractor -> Storage: save API structure
   User -> Ladar: compare structures
   Ladar -> Comparator: run comparison algorithms
   Comparator -> Storage: save comparison result
   User -> Ladar: apply mapping
   Ladar -> Substitutor: apply substitution to project
   @enduml

This diagram shows how the user initiates actions and how Ladar processes these requests
through its core components.

Component Diagram
-----------------

The component diagram shows the key components of Ladar and how they interact with each
other. Each component is responsible for a specific task, such as extracting APIs,
comparing structures, and generating mappings for substitution.

.. graphviz::

   digraph G {
      "Extractor" -> "Comparator" [label="compare extracted APIs"];
      "Comparator" -> "Mapping Generator" [label="generate mapping"];
      "Mapping Generator" -> "Substitutor" [label="apply mapping to project"];
   }

   subgraph cluster_0 {
      label="Ladar Core Components";
      "Extractor";
      "Comparator";
      "Mapping Generator";
      "Substitutor";
   }

This diagram highlights the key components:

- the **Extractor** handles API extraction, see the :ref:`extract-cmd` page.
- the **Comparator** compares the extracted APIs, see the :ref:`compare-cmd` page.
- the **Mapping Generator** creates mappings for substitution,
- and the **Substitutor** applies the mapping.

Processing Pipeline Diagram
---------------------------

This pipeline diagram provides an overview of the data flow through Ladar. The process
begins with API structure input, followed by extraction, normalization, comparison, and
finally, substitution.

.. graphviz::

   digraph G {
      "APIs Structures" -> "Extraction" -> "Normalization" -> "Comparison" -> "Mapping" -> "Substitution";
   }

Each step in this pipeline represents a phase in the Ladar process, showing how data
flows from one operation to the next, ultimately leading to the substitution of API
structures within a project.

Conclusion
----------

These diagrams illustrate the various aspects of Ladar, from its overall process to the
detailed interactions between its components. Ladar provides a powerful and flexible way
to manage API extraction, comparison, and substitution in Python projects.
