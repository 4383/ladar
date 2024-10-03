import pytest

from ladar.api.pipeline import parse_step


def test_parse_step_no_params():
    """Test parsing a step with no parameters."""
    step_str = "normalize:MinMaxScaler"
    algorithm_name = parse_step(step_str)
    assert (
        algorithm_name == "minmaxscaler"
    ), "Algorithm name should be normalized to lowercase."
