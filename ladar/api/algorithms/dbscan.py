import numpy as np
from sklearn.cluster import DBSCAN


def add_arguments(parser):
    """
    Add DBSCAN-specific arguments to the parser.
    """
    parser.add_argument(
        "--dbscan-eps",
        type=float,
        default=0.5,
        help="DBSCAN: The maximum distance between two samples (eps).",
    )
    parser.add_argument(
        "--dbscan-min_samples",
        type=int,
        default=2,
        help="DBSCAN: The number of samples in a neighborhood for a point to be a core point.",
    )


def create_similarity_matrix(structures):
    num_structures = len(structures)
    similarity_matrix = np.zeros((num_structures, num_structures))

    for i in range(num_structures):
        for j in range(num_structures):
            similarity_matrix[i][j] = 1.0 - abs(
                len(structures[i]) - len(structures[j])
            ) / max(len(structures[i]), len(structures[j]))

    return similarity_matrix


def compare(structures: list, params: dict = None) -> dict:
    eps = params.get("eps", 0.5)
    min_samples = params.get("min_samples", 2)

    similarity_matrix = create_similarity_matrix(structures)

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed").fit(
        similarity_matrix
    )

    return {
        "algorithm_used": "dbscan",
        "similarity_score": clustering.labels_.tolist(),
        "mapping": {
            "clusters": clustering.labels_.tolist(),
        },
        "additional_info": {
            "eps": eps,
            "min_samples": min_samples,
        },
    }
