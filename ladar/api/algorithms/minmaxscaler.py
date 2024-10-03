# ladar/api/algorithms/minmaxscaler.py
import logging

from ladar.api.algorithms.base import AlgorithmCategory, BaseAlgorithm

logger = logging.getLogger(__name__)


class MinMaxScaler(BaseAlgorithm):
    """
    MinMaxScaler normalizes data by scaling the feature values to a specified range, usually [0, 1].
    """

    category = AlgorithmCategory.NORMALIZATION

    def __init__(self, feature_range=(0, 1)):
        """
        Initialize the MinMaxScaler with a feature range.

        Args:
            feature_range (tuple): Desired range of transformed data (min, max).
        """
        self.feature_range = feature_range

    @staticmethod
    def add_arguments(parser):
        """
        Add specific arguments for the MinMaxScaler algorithm to the parser.

        Args:
            parser (argparse.ArgumentParser): The argument parser.
        """
        parser.add_argument(
            "--minmaxscaler-feature_range",
            type=float,
            nargs=2,
            default=(0, 1),
            help="Range for scaling. Two values expected: min and max. Default is (0, 1).",
        )

    def fit(self, structures):
        """
        Fit the MinMaxScaler to the data. Initialize min and max values in the data.

        Args:
            structures (list): List of input structures to be fitted.
        """
        logger.debug(f"Raw structures: {structures}")

        flat_values = self._flatten_structure(structures)

        # Log de débogage pour voir les valeurs extraites
        logger.debug(f"Flattened values: {flat_values}")

        if not flat_values:
            raise ValueError("The structure contains no numeric values to scale.")

        self.data_min_ = min(flat_values)
        self.data_max_ = max(flat_values)

    def transform(self, structures):
        """
        Apply the MinMaxScaler to transform the data within the specified range.

        Args:
            structures (list): List of input structures to be transformed.

        Returns:
            list: List of scaled structures.
        """
        scaled_structures = []

        for structure in structures:
            scaled_structure = self._scale_structure(
                structure, self.feature_range[0], self.feature_range[1]
            )
            scaled_structures.append(scaled_structure)

        return scaled_structures

    def fit_transform(self, structures):
        """
        Fit to data, then transform it.

        Args:
            structures (list): List of input structures to fit and transform.

        Returns:
            list: List of scaled structures.
        """
        self.fit(structures)
        return self.transform(structures)

    def _scale_structure(self, structure, min_val, max_val):
        """
        Scale a structure's numeric values to the specified range.

        Args:
            structure (dict): The structure containing numeric values.
            min_val (float): Minimum value of the desired range.
            max_val (float): Maximum value of the desired range.

        Returns:
            dict: The scaled structure.
        """
        # Find the min and max values in the structure
        flat_values = self._flatten_structure(structure)
        original_min = min(flat_values)
        original_max = max(flat_values)

        # Normalize each value
        def scale_value(value):
            return min_val + (value - original_min) * (max_val - min_val) / (
                original_max - original_min
            )

        return self._apply_scaling(structure, scale_value)

    def _flatten_structure(self, structure):
        """
        Flatten the numeric values in a nested structure (dict or list) to a single list.

        Args:
            structure (any): The nested structure containing numeric values.

        Returns:
            list: A list of all numeric values found in the structure.
        """
        flat_values = []

        if isinstance(structure, dict):
            for value in structure.values():
                flat_values.extend(self._flatten_structure(value))
        elif isinstance(structure, list):
            for item in structure:
                flat_values.extend(self._flatten_structure(item))
        elif isinstance(structure, (int, float)):
            flat_values.append(structure)

        return flat_values

    def _apply_scaling(self, structure, scale_func):
        """
        Recursively apply the scaling function to the structure.

        Args:
            structure (any): The structure to scale.
            scale_func (function): The function to scale each value.

        Returns:
            any: The scaled structure.
        """
        if isinstance(structure, dict):
            return {
                key: self._apply_scaling(value, scale_func)
                for key, value in structure.items()
            }
        elif isinstance(structure, list):
            return [self._apply_scaling(item, scale_func) for item in structure]
        elif isinstance(structure, (int, float)):
            return scale_func(structure)

        return structure
