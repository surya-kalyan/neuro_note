import os
import datetime
from utils.logger import logger
from utils.error_handlers import FileStorageError

OUTPUT_BASE_DIR = "output/meetings"

def ensure_dir_exists(directory_path):
    """Ensures that the specified directory exists, creating it if necessary."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory_path}")
    except OSError as e:
        logger.error(f"Error creating directory {directory_path}: {e}", exc_info=True)
        raise FileStorageError(f"Could not create directory {directory_path}: {e}")

def save_text_to_file(content, filename, subdirectory=""):
    """
    Saves the given text content to a file in a specified subdirectory under OUTPUT_BASE_DIR.
    A timestamped parent directory will be created for each session.
    """
    try:
        # Create a unique directory for this session based on timestamp
        # The 'subdirectory' here is intended to be the meeting_id for grouping.
        session_dir = os.path.join(OUTPUT_BASE_DIR, subdirectory) # subdirectory is meeting_id
        ensure_dir_exists(session_dir)

        file_path = os.path.join(session_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Successfully saved content to {file_path}")
        return file_path
    except FileStorageError: # Already logged in ensure_dir_exists
        raise
    except IOError as e:
        logger.error(f"IOError saving content to file {filename} in {session_dir}: {e}", exc_info=True)
        raise FileStorageError(f"Could not write to file {filename}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving content to file {filename} in {session_dir}: {e}", exc_info=True)
        raise FileStorageError(f"An unexpected error occurred while saving file {filename}: {e}")

def save_transcript(transcript_text, meeting_id="meeting"):
    """Saves the transcript text to a file, named with meeting_id."""
    # The actual filename will be like 'meeting_20231027_103000_transcript.txt'
    # And it will be inside a directory named 'meeting_20231027_103000'
    filename = f"{meeting_id}_transcript.txt"
    return save_text_to_file(transcript_text, filename, subdirectory=meeting_id)

def save_insights(insights_text, meeting_id="meeting"):
    """Saves the insights text to a file, named with meeting_id."""
    filename = f"{meeting_id}_insights.md" # Using .md for better readability of structured insights
    return save_text_to_file(insights_text, filename, subdirectory=meeting_id)
