import whisper
import os

# Attempt to import config, handle if it's not found for some reason (e.g. testing environment)
try:
    from config import DEFAULT_WHISPER_MODEL
except ImportError:
    logger.warning("config.py not found, using default WHISPER_MODEL='base'.")
    DEFAULT_WHISPER_MODEL = "base" # Fallback if config.py is not found

# Import custom error and logger
from utils.error_handlers import TranscriptionError
from utils.logger import logger

# --- Whisper Setup ---
# Use environment variable for model name if set, otherwise use config default
WHISPER_MODEL_NAME = os.environ.get("WHISPER_MODEL", DEFAULT_WHISPER_MODEL)
logger.info(f"Initializing Whisper model: {WHISPER_MODEL_NAME}")
model = None
try:
    model = whisper.load_model(WHISPER_MODEL_NAME)
    logger.info(f"Whisper model '{WHISPER_MODEL_NAME}' loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load Whisper model '{WHISPER_MODEL_NAME}': {e}. Attempting fallback to 'base' model.", exc_info=True)
    if WHISPER_MODEL_NAME != "base": # Avoid trying to load base model twice if it was the one that failed
        try:
            WHISPER_MODEL_NAME = "base" # Explicitly set to base for logging clarity on fallback
            model = whisper.load_model(WHISPER_MODEL_NAME)
            logger.info(f"Successfully loaded fallback Whisper model '{WHISPER_MODEL_NAME}'.")
        except Exception as e_fallback:
            logger.critical(f"Failed to load even the fallback Whisper model '{WHISPER_MODEL_NAME}': {e_fallback}", exc_info=True)
            raise TranscriptionError(f"Could not initialize Whisper model: {e_fallback}")
    else: # Original model was 'base' and it failed
        logger.critical(f"Failed to load the primary Whisper model '{WHISPER_MODEL_NAME}': {e}", exc_info=True)
        raise TranscriptionError(f"Could not initialize Whisper model '{WHISPER_MODEL_NAME}': {e}")


def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using the configured Whisper model.
    """
    if not model:
        logger.error("Whisper model is not available or failed to load prior to transcription call.")
        raise TranscriptionError("Whisper model is not available or failed to load.")

    logger.info(f"Starting transcription for audio file: {file_path} using model: {WHISPER_MODEL_NAME}")
    try:
        result = model.transcribe(file_path)
        transcript = result["text"]
        logger.info(f"Transcription completed for {file_path}. Transcript length: {len(transcript)} chars.")
        logger.debug(f"Transcript snippet: {transcript[:100]}...") # Log a snippet for debugging
        return transcript
    except Exception as e:
        logger.error(f"Error during Whisper transcription for {file_path}: {e}", exc_info=True)
        raise TranscriptionError(f"Whisper transcription failed for {file_path}: {e}")
