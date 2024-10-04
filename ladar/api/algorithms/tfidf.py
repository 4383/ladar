# ladar/api/algorithms/tfidf.py

from sklearn.feature_extraction.text import TfidfVectorizer

from ladar.api.algorithms.base import AlgorithmCategory, BaseAlgorithm


class TFIDF(BaseAlgorithm):
    """
    TF-IDF algorithm extracts and compares textual features from API structures using Term Frequency-Inverse Document Frequency.
    """

    category = AlgorithmCategory.FEATURE_EXTRACTION

    def __init__(self, max_features=500, stop_words="english"):
        """
        Initialize the TF-IDF algorithm with specified parameters.

        Args:
            max_features (int): Maximum number of features (terms) to extract.
            stop_words (str or list): Stop words to ignore in text processing. Default is "english".
        """
        self.max_features = max_features
        self.stop_words = stop_words
        self.vectorizer = (
            None  # The TfidfVectorizer will be initialized in the fit method
        )

    @staticmethod
    def add_arguments(parser):
        """
        Add specific arguments for the TF-IDF algorithm to the parser.

        Args:
            parser (argparse.ArgumentParser): The argument parser.
        """
        parser.add_argument(
            "--tfidf-max_features",
            type=int,
            default=500,
            help="Maximum number of features to extract. Default is 500.",
        )
        parser.add_argument(
            "--tfidf-stop_words",
            type=str,
            default="english",
            help='Stop words to ignore in text processing. Default is "english".',
        )

    def fit(self, structures):
        """
        Fit the TF-IDF model to the input structures (API textual data).

        Args:
            structures (list): List of input structures (API descriptions).
        """
        # Flatten the structures into a list of text documents
        documents = [self._structure_to_text(structure) for structure in structures]

        # Initialize the TfidfVectorizer and fit it to the documents
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features, stop_words=self.stop_words
        )
        self.vectorizer.fit(documents)

    def transform(self, structures):
        """
        Apply the fitted TF-IDF model to transform the input structures into TF-IDF vectors.

        Args:
            structures (list): List of input structures (API descriptions).

        Returns:
            dict: Dictionary containing the TF-IDF feature vectors for each structure.
        """
        documents = [self._structure_to_text(structure) for structure in structures]
        tfidf_matrix = self.vectorizer.transform(documents)

        return {
            "tfidf_features": tfidf_matrix.toarray(),
            "feature_names": self.vectorizer.get_feature_names_out(),
        }

    def fit_transform(self, structures):
        """
        Fit the TF-IDF model and transform the input structures into TF-IDF vectors.

        Args:
            structures (list): List of input structures (API descriptions).

        Returns:
            dict: Dictionary containing the TF-IDF feature vectors for each structure.
        """
        self.fit(structures)
        return self.transform(structures)

    def _structure_to_text(self, structure):
        """
        Convert an API structure into a concatenated string of its key components.

        Args:
            structure (dict): The structure representing an API or its components.

        Returns:
            str: A text representation of the structure.
        """
        if isinstance(structure, dict):
            return " ".join(
                self._structure_to_text(value) for value in structure.values()
            )
        elif isinstance(structure, list):
            return " ".join(self._structure_to_text(item) for item in structure)
        elif isinstance(structure, str):
            return structure
        else:
            return str(structure)
