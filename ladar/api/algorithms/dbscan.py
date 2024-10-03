import logging

import Levenshtein
import numpy as np
from sklearn.cluster import DBSCAN

logger = logging.getLogger(__name__)


# ladar/algorithms/dbscan.py

from ladar.api.algorithms.base import AlgorithmCategory, BaseAlgorithm


class DBSCAN(BaseAlgorithm):
    """
    DBSCAN clustering algorithm.
    """

    category = AlgorithmCategory.CLUSTERING

    def __init__(self, eps=0.5, min_samples=5):
        super().__init__(eps=eps, min_samples=min_samples)
        self.eps = eps
        self.min_samples = min_samples

    def fit(self, data):
        # Implémentation du fitting pour DBSCAN
        pass

    def transform(self, data):
        # Implémentation de la transformation après le fit pour DBSCAN
        pass

    @staticmethod
    def add_arguments(parser):
        """
        Add DBSCAN-specific arguments to the parser.
        """
        parser.add_argument(
            "--dbscan-eps", type=float, default=0.5, help="DBSCAN epsilon parameter"
        )
        parser.add_argument(
            "--dbscan-min_samples", type=int, default=5, help="DBSCAN minimum samples"
        )


# def add_arguments(parser):
#    """
#    Add DBSCAN-specific arguments to the parser.
#
#    Parameters for the DBSCAN algorithm:
#
#    - `eps`: The maximum distance between two samples for one to be considered as
#      in the neighborhood of the other. Smaller values of `eps` result in smaller,
#      denser clusters. Default is `0.5`.
#
#    - `min_samples`: The number of samples (or total weight) in a neighborhood for
#      a point to be considered a core point. This includes the point itself. Higher
#      values of `min_samples` make the algorithm more conservative in forming clusters.
#      Default is `2`.
#
#    These parameters control how the DBSCAN algorithm clusters the API structures.
#
#    Args:
#        parser (argparse.ArgumentParser): The argument parser instance where the DBSCAN-specific
#                                          options are added.
#    """
#    parser.add_argument(
#        "--dbscan-eps",
#        type=float,
#        default=0.5,
#        help="DBSCAN: The maximum distance between two samples (eps).",
#    )
#    parser.add_argument(
#        "--dbscan-min_samples",
#        type=int,
#        default=2,
#        help="DBSCAN: The number of samples in a neighborhood for a point to be a core point.",
#    )
#
#
# def create_similarity_matrix(elements):
#    """
#    Create a similarity matrix based on the Levenshtein distance between
#    element names, signatures, and docstrings.
#
#    Args:
#        elements (list): List of all elements (from all structures) to compare.
#
#    Returns:
#        numpy.ndarray: A matrix representing similarities between the elements.
#    """
#    num_elements = len(elements)
#    if num_elements == 0:
#        raise ValueError("No elements found in the structures for comparison.")
#
#    similarity_matrix = np.zeros((num_elements, num_elements))
#
#    for i in range(num_elements):
#        for j in range(num_elements):
#            if i == j:
#                similarity_matrix[i][j] = 0
#            else:
#                # Extract the names, docstrings, and signatures (if available)
#                name_i = (
#                    elements[i]["name"]
#                    if isinstance(elements[i], dict)
#                    else elements[i]
#                )
#                name_j = (
#                    elements[j]["name"]
#                    if isinstance(elements[j], dict)
#                    else elements[j]
#                )
#
#                doc_i = (
#                    elements[i].get("docstring", "")
#                    if isinstance(elements[i], dict)
#                    else ""
#                )
#                doc_j = (
#                    elements[j].get("docstring", "")
#                    if isinstance(elements[j], dict)
#                    else ""
#                )
#
#                signature_i = (
#                    elements[i].get("signature", "")
#                    if isinstance(elements[i], dict)
#                    else ""
#                )
#                signature_j = (
#                    elements[j].get("signature", "")
#                    if isinstance(elements[j], dict)
#                    else ""
#                )
#
#                # Combine name, docstring, and signature for similarity calculation
#                combined_i = name_i + " " + signature_i + " " + doc_i
#                combined_j = name_j + " " + signature_j + " " + doc_j
#
#                # Calculate Levenshtein distance between the combined strings
#                lev_distance = Levenshtein.distance(combined_i, combined_j)
#                max_length = max(len(combined_i), len(combined_j))
#
#                if max_length == 0:
#                    similarity_matrix[i][j] = 0
#                else:
#                    similarity_matrix[i][j] = lev_distance / max_length
#
#    if np.isnan(similarity_matrix).any() or np.isinf(similarity_matrix).any():
#        raise ValueError("Similarity matrix contains NaN or infinity values.")
#
#    logger.info(f"Similarity matrix calculated: {similarity_matrix}")
#    return similarity_matrix
#
#
# def generate_mapping(detailed_mapping):
#    """
#    Generates a mapping based on the clusters assigned by DBSCAN.
#
#    Args:
#        detailed_mapping (dict): A dictionary with elements and their corresponding clusters.
#
#    Returns:
#        dict: A mapping that associates similar elements from different structures within each cluster.
#    """
#    cluster_mapping = {}
#
#    for structure, elements in detailed_mapping.items():
#        for element, cluster in elements.items():
#            if cluster not in cluster_mapping:
#                cluster_mapping[cluster] = []
#            cluster_mapping[cluster].append({structure: element})
#
#    return cluster_mapping
#
#
# def filter_elements(elements):
#    """
#    Filters the relevant elements in the structure to keep only
#    functions, methods, and classes. Excludes nested modules and
#    members without useful information.
#
#    Args:
#        elements (dict): Dictionary of extracted elements from the structures.
#
#    Returns:
#        list: Filtered list of relevant elements (functions, methods, classes).
#    """
#    filtered_elements = []
#    for element_name, element_info in elements.items():
#        if element_info["type"] in ["class", "function", "method"]:
#            filtered_elements.append(element_name)
#    return filtered_elements
#
#
# def compare(structures: list, params: dict = None) -> dict:
#    """
#    Compare API structures using the DBSCAN algorithm and return clusters.
#
#    Args:
#        structures (list): List of API structures to compare.
#        params (dict): Parameters for the DBSCAN algorithm (eps, min_samples).
#
#    Returns:
#        dict: A dictionary containing the comparison results, clusters, detailed mapping, and automatic cluster mapping.
#    """
#    if not structures or any(len(structure) == 0 for structure in structures):
#        raise ValueError("One or more structures are empty or missing.")
#
#    eps = params.get("eps", 0.5)
#    min_samples = params.get("min_samples", 2)
#
#    all_elements = []
#    structure_mapping = []
#    for i, structure in enumerate(structures):
#        filtered_structure = filter_elements(structure)
#        all_elements.extend(filtered_structure)
#        structure_mapping.extend([f"struct_{i+1}"] * len(filtered_structure))
#
#    logger.info(f"All elements merged after filtering: {all_elements}")
#
#    similarity_matrix = create_similarity_matrix(all_elements)
#
#    try:
#        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed").fit(
#            similarity_matrix
#        )
#    except Exception as e:
#        logger.error(f"DBSCAN failed with error: {e}")
#        raise e
#
#    labels = clustering.labels_.astype(int).tolist()
#
#    if len(labels) != len(all_elements):
#        raise ValueError(
#            f"Mismatch between labels and elements: {len(labels)} labels for {len(all_elements)} elements"
#        )
#
#    detailed_mapping = {}
#    label_index = 0
#    for i, structure in enumerate(structures):
#        filtered_structure = filter_elements(structure)
#        detailed_mapping[f"struct_{i+1}"] = {}
#
#        for idx in range(len(filtered_structure)):
#            element_name = filtered_structure[idx]
#            detailed_mapping[f"struct_{i+1}"][element_name] = labels[label_index]
#            label_index += 1
#
#    cluster_mapping = generate_mapping(detailed_mapping)
#
#    return {
#        "algorithm_used": "dbscan",
#        "similarity_score": labels,
#        "mapping": {
#            "clusters": labels,
#        },
#        "detailed_mapping": detailed_mapping,
#        "cluster_mapping": cluster_mapping,
#        "additional_info": {
#            "eps": eps,
#            "min_samples": min_samples,
#        },
#    }
