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
    Test that docstrings are correctly normalized to lowercase without removing spaces or special characters.

    This function verifies:
    - Docstrings are converted to lowercase.
    - Spaces, newlines, and special characters remain unchanged.
    """
    # Test cases
    docstring = "This is A Test Docstring.\nWith New Lines and SPECIAL Characters!"
    expected_result = (
        "this is a test docstring.\nwith new lines and special characters!"
    )

    assert (
        normalize_docstring(docstring) == expected_result
    ), "Docstring should be converted to lowercase without altering spaces or special characters"

    # Test with an empty string
    assert (
        normalize_docstring("") == ""
    ), "Empty docstring should return an empty string"

    # Test with None (should return None)
    assert normalize_docstring(None) is None, "None input should return None"
