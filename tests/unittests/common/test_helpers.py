import argparse

from ladar.common.helpers import build_algorithm_params


def test_build_algorithm_params():
    """
    Test that the build_algorithm_params function correctly builds a dictionary of parameters.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbscan-eps", type=float)
    parser.add_argument("--dbscan-min_samples", type=int)
    parser.add_argument("--tfidf-max_features", type=int)

    args = parser.parse_args(
        [
            "--dbscan-eps",
            "0.3",
            "--dbscan-min_samples",
            "4",
            "--tfidf-max_features",
            "1000",
        ]
    )

    params = build_algorithm_params(args)

    assert "dbscan" in params
    assert params["dbscan"]["eps"] == 0.3
    assert params["dbscan"]["min_samples"] == 4
    assert "tfidf" in params
    assert params["tfidf"]["max_features"] == 1000
