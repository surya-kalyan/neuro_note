import os
import datetime # For generating a unique meeting ID
from flask import Flask, request, jsonify
from flask_cors import CORS

# Logger first
from utils.logger import logger

# Attempt to import config, with fallbacks for DEBUG
try:
    from config import DEBUG
except ImportError:
    logger.warning("config.py not found, using default DEBUG=True.")
    DEBUG = True

# Import services
from services.transcription import transcribe_audio
from services.gemini import generate_insights
from services.storage_service import save_transcript, save_insights, OUTPUT_BASE_DIR # Modified import

# Import error handlers and custom exceptions
from utils.error_handlers import (
    AppError,
    TranscriptionError,
    GeminiError,
    FileStorageError,
    handle_app_error,
    handle_generic_error,
    handle_not_found_error
)

app = Flask(__name__)
CORS(app)
logger.info("Flask app initialized with CORS.")

# Ensure base output directory exists at startup
try:
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    logger.info(f"Ensured base output directory exists: {OUTPUT_BASE_DIR}")
except OSError as e:
    logger.error(f"Could not create base output directory {OUTPUT_BASE_DIR} at startup: {e}", exc_info=True)
    # Depending on how critical this is, you might want to exit or raise an error.
    # For now, just logging, as individual save calls will also try to create dirs.

# Register error handlers
app.register_error_handler(AppError, handle_app_error)
logger.info("Registered AppError handler.")
app.register_error_handler(404, handle_not_found_error)
logger.info("Registered 404 error handler.")
app.register_error_handler(Exception, handle_generic_error)
logger.info("Registered generic Exception handler.")


@app.route('/recorded-audio', methods=['POST'])
def handle_audio():
    logger.info(f"Received request for /recorded-audio from {request.remote_addr}")

    if 'file' not in request.files:
        logger.warning("No file part in the request.")
        raise AppError("No file part in the request.", status_code=400)

    file = request.files['file']
    if file.filename == '':
        logger.warning("No selected file (empty filename).")
        raise AppError("No selected file.", status_code=400)

    # Generate a unique meeting ID for this session for file naming and directory creation
    meeting_id = f"meeting_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    # Temporary path for the uploaded audio file.
    # Using a temporary directory or a dedicated uploads directory might be better in a real scenario.
    temp_audio_file_path = f'./{meeting_id}_uploaded_audio.wav' # Stored in root for now
    logger.debug(f"Attempting to save uploaded file '{file.filename}' temporarily to '{temp_audio_file_path}'")

    try:
        file.save(temp_audio_file_path)
        logger.info(f"File '{file.filename}' saved successfully to temporary path '{temp_audio_file_path}'")

        logger.info(f"Starting audio processing for meeting_id: {meeting_id} (source file: {temp_audio_file_path})...")
        transcript = transcribe_audio(temp_audio_file_path)

        logger.info(f"Starting insight generation for meeting_id: {meeting_id}...")
        insights = generate_insights(transcript)

        logger.info(f"Successfully processed audio and generated insights for meeting_id: {meeting_id}.")

        # Save transcript and insights using the storage service
        try:
            logger.info(f"Attempting to save transcript for meeting_id: {meeting_id}")
            transcript_path = save_transcript(transcript, meeting_id)
            logger.info(f"Transcript for meeting_id {meeting_id} saved to: {transcript_path}")

            logger.info(f"Attempting to save insights for meeting_id: {meeting_id}")
            insights_path = save_insights(insights, meeting_id)
            logger.info(f"Insights for meeting_id {meeting_id} saved to: {insights_path}")
        except FileStorageError as fse:
            logger.error(f"File storage error when saving outputs for meeting_id {meeting_id}: {fse.message}", exc_info=True)
            # Not re-raising, as successful processing but failed saving might still be a partial success for the user.
            # The main response with insights will still be returned.
        except Exception as e_save:
            logger.error(f"Unexpected error during saving transcript/insights for meeting_id {meeting_id}: {e_save}", exc_info=True)
            # Also not re-raising this for now.

        return jsonify({
            "status" : "success",
            "text" : insights,
            "meetingId": meeting_id, # Return the meeting_id
            "transcriptPath": transcript_path if 'transcript_path' in locals() else None, # Return paths if saved
            "insightsPath": insights_path if 'insights_path' in locals() else None
        })

    except TranscriptionError as e:
        logger.error(f"TranscriptionError caught in handle_audio for meeting_id {meeting_id} (file: {file.filename}): {e.message}", exc_info=True)
        raise e
    except GeminiError as e:
        logger.error(f"GeminiError caught in handle_audio for meeting_id {meeting_id} (file: {file.filename}): {e.message}", exc_info=True)
        raise e
    except FileStorageError as e: # If file.save() itself fails, for instance.
        logger.error(f"FileStorageError (e.g., initial save) caught in handle_audio for meeting_id {meeting_id} (file: {file.filename}): {e.message}", exc_info=True)
        raise e # This is likely critical if we can't even save the upload.
    except AppError as e:
        logger.error(f"Unhandled AppError caught in handle_audio for meeting_id {meeting_id} (file: {file.filename}): {e.message}", exc_info=True)
        raise e
    except Exception as e:
        logger.error(f"An unexpected non-AppError exception occurred in handle_audio for meeting_id {meeting_id} (file: {file.filename}): {str(e)}", exc_info=True)
        raise AppError(f"An unexpected server error occurred processing file '{file.filename}'.", status_code=500)

    finally:
        if os.path.exists(temp_audio_file_path):
            try:
                logger.debug(f"Attempting to delete temporary uploaded audio file: {temp_audio_file_path}")
                os.remove(temp_audio_file_path)
                logger.info(f"Cleaned up temporary uploaded audio file: {temp_audio_file_path}")
            except Exception as e_cleanup:
                logger.error(f"Error deleting temporary audio file {temp_audio_file_path}: {e_cleanup}", exc_info=True)


if __name__ == "__main__":
    logger.info("Starting NeuroNote application directly...")

    flask_debug_env = os.environ.get("FLASK_DEBUG")
    if flask_debug_env is not None:
        effective_debug = flask_debug_env.lower() in ['true', '1', 't']
    else:
        effective_debug = DEBUG
    logger.info(f"Flask effective debug mode: {effective_debug}")

    host = os.environ.get("FLASK_RUN_HOST", '0.0.0.0')
    port = int(os.environ.get("FLASK_RUN_PORT", os.environ.get("PORT", 5000)))

    logger.info(f"Attempting to start Flask app on {host}:{port}")
    app.run(debug=effective_debug, host=host, port=port)
