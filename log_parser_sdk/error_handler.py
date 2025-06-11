class ErrorHandler:
    def handle_error(self, error: Exception, message: str = "An error occurred"):
        """
        Handles errors by printing an error message and raising the exception.
        """
        print(f"Error: {message}: {error}")
        raise error


