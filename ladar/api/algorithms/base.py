# ladar/algorithms/base.py

from enum import Enum, auto


class AlgorithmCategory(Enum):
    """
    Enumeration for standardizing algorithm categories.
    """

    CLUSTERING = "clustering"
    DIMENSION_REDUCTION = "dimension_reduction"
    FEATURE_EXTRACTION = "feature_extraction"
    TRANSFORMATION = "transformation"
    NORMALIZATION = "normalization"


class BaseAlgorithm:
    """
    Base class for all algorithms in Ladar.

    Attributes:
        category (AlgorithmCategory): The category of the algorithm (e.g., clustering, transformation).
    """

    category = None  # To be defined in the child classes

    def __init__(self, **params):
        """
        Initialize the algorithm with its parameters.

        Args:
            **params: The parameters specific to the algorithm.
        """
        self.params = params

    def fit(self, data):
        """
        Placeholder for fitting the algorithm to the data.

        Args:
            data: The input data for the algorithm.
        """
        raise NotImplementedError("The fit method should be implemented by subclasses.")

    def transform(self, data):
        """
        Placeholder for transforming data after fitting.

        Args:
            data: The input data to transform.

        Returns:
            Transformed data.
        """
        raise NotImplementedError(
            "The transform method should be implemented by subclasses."
        )

    def fit_transform(self, data):
        """
        Fit the algorithm to the data and then transform it.

        Args:
            data: The input data for the algorithm.

        Returns:
            Transformed data.
        """
        self.fit(data)
        return self.transform(data)

    @staticmethod
    def add_arguments(parser):
        """
        Add command-line arguments specific to the algorithm.

        This method should be implemented in subclasses.

        Args:
            parser (argparse.ArgumentParser): Argument parser for adding algorithm-specific arguments.
        """
        raise NotImplementedError("Subclasses should implement add_arguments method.")
