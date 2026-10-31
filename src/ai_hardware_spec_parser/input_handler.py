class InputHandler:
    """
    Handles accepting plain text hardware specs as input.
    """

    def __init__(self):
        self.raw_text = None

    def accept_text(self, text):
        """
        Accepts plain text hardware specs as input.
        Args:
            text (str): The plain text hardware specification.
        Returns:
            None
        Raises:
            ValueError: If input is not a string or is empty.
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        if not text.strip():
            raise ValueError("Input text cannot be empty.")
        self.raw_text = text

    def get_text(self):
        """
        Returns the stored hardware spec text.
        Returns:
            str: The stored plain text hardware specification.
        """
        return self.raw_text
