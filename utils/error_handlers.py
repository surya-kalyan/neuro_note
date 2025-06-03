from flask import jsonify, request # Added request
from utils.logger import logger # Import logger

class AppError(Exception):
    """Base application error class."""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def to_dict(self):
        return {"status": "error", "message": self.message}

class TranscriptionError(AppError):
    """Custom error for transcription failures."""
    def __init__(self, message="Error during audio transcription."):
        super().__init__(message, status_code=500)

class GeminiError(AppError):
    """Custom error for Gemini API failures."""
    def __init__(self, message="Error generating insights with Gemini."):
        super().__init__(message, status_code=500)

class FileStorageError(AppError):
    """Custom error for file storage operations."""
    def __init__(self, message="Error during file storage operation."):
        super().__init__(message, status_code=500)

def handle_app_error(error):
    """Handles AppError and its subclasses."""
    # Log with exc_info=True to include stack trace for unexpected AppErrors if they don't originate from explicit "raise AppError(...)"
    logger.error(f"AppError caught: {error.message} (Status code: {error.status_code})", exc_info=isinstance(error, AppError) and error.status_code == 500)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_generic_error(error):
    """Handles generic exceptions."""
    logger.critical(f"Unhandled generic exception caught: {str(error)}", exc_info=True)
    response = jsonify({"status": "error", "message": "An unexpected internal server error occurred."})
    response.status_code = 500
    return response

def handle_not_found_error(error):
    """Handles 404 Not Found errors."""
    logger.warning(f"404 Not Found error: {error}. Requested URL: {request.url if request else 'N/A'}")
    response = jsonify({"status": "error", "message": "The requested resource was not found."})
    response.status_code = 404
    return response
