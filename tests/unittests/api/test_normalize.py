import pytest

from ladar.api.normalize import normalize_content, normalize_docstring


@pytest.mark.parametrize(
    "input_content, expected_output",
    [
        # Test simple lowercase conversion and space removal
        ({"name": "John_Doe"}, {"name": "johndoe"}),
        # Test conversion with camelCase and space removal
        ({"userName": "JohnDoe"}, {"username": "johndoe"}),
        # Test with a combination of underscores and camelCase
        ({"SomeName": "John_Doe"}, {"somename": "johndoe"}),
        # Test nested dictionaries with space removal
        (
            {"Person": {"FirstName": "John", "Last_Name": "Doe"}},
            {"person": {"firstname": "john", "lastname": "doe"}},
        ),
        # Test lists inside dictionaries with space removal
        (
            {
                "Users": [
                    {"FirstName": "John", "LastName": "Doe"},
                    {"FirstName": "Jane", "LastName": "Smith"},
                ]
            },
            {
                "users": [
                    {"firstname": "john", "lastname": "doe"},
                    {"firstname": "jane", "lastname": "smith"},
                ]
            },
        ),
        # Test empty dictionary
        ({}, {}),
        # Test with numbers and special characters that should remain unchanged
        (
            {"Age": 30, "Email_Address": "john.doe@example.com"},
            {"age": 30, "emailaddress": "john.doe@example.com"},
        ),
    ],
)
def test_normalize_content(input_content, expected_output):
    """
    Test the normalize_content function with various inputs and expected outputs.
    """
    assert normalize_content(input_content) == expected_output


def test_normalize_docstring():
    """
    Test that docstrings are correctly normalized to lowercase and formatted as a single, compact string.

    This function verifies:
    - Docstrings are converted to lowercase.
    - Newlines and excessive spaces are replaced with a single space.
    - Special characters and meaningful spaces are preserved.
    """

    # Test case with multiple lines and extra spaces
    docstring = """Number of ways to choose k items from n items without repetition and
    with order.

    Evaluates to n! / (n - k)! when k <= n and evaluates

    to zero when k > n.

    If k is not specified or is None, then k defaults to n

    and the function returns n!.

    Raises TypeError if either of the arguments are not integers.

    Raises ValueError if either of the arguments are negative."""

    expected_result = (
        "number of ways to choose k items from n items without repetition and with order. "
        "evaluates to n! / (n - k)! when k <= n and evaluates to zero when k > n. "
        "if k is not specified or is none, then k defaults to n and the function returns n!. "
        "raises typeerror if either of the arguments are not integers. "
        "raises valueerror if either of the arguments are negative."
    )

    assert (
        normalize_docstring(docstring) == expected_result
    ), "Docstring should be normalized by converting to lowercase and removing excessive newlines and spaces"

    # Test with an empty string
    assert (
        normalize_docstring("") == ""
    ), "Empty docstring should return an empty string"

    # Test with None (should return None)
    assert normalize_docstring(None) is None, "None input should return None"
