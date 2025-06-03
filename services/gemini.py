import google.generativeai as genai
import os

# Attempt to import config, handle if it's not found
try:
    from config import DEFAULT_GEMINI_MODEL, GEMINI_API_KEY as CONFIG_GEMINI_API_KEY
except ImportError:
    logger.warning("config.py not found, using default GEMINI_MODEL and no API key from config.")
    DEFAULT_GEMINI_MODEL = "models/gemini-1.5-flash-latest"
    CONFIG_GEMINI_API_KEY = None

# Import custom error and logger
from utils.error_handlers import GeminiError
from utils.logger import logger

# --- Gemini Setup ---
# Prioritize environment variable for API key, then config file
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    logger.info("GEMINI_API_KEY not found in environment variables. Trying config.py.")
    api_key = CONFIG_GEMINI_API_KEY
    if api_key:
        logger.info("Loaded GEMINI_API_KEY from config.py.")

if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables or config.py. This is a critical setup error.")
    # This is a critical setup error, so raise EnvironmentError directly or a specific AppError.
    raise GeminiError("GEMINI_API_KEY not found in environment variables or config.py. Please set it.", status_code=500)

try:
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")
except Exception as e:
    logger.error(f"Failed to configure Gemini API with the provided key: {e}", exc_info=True)
    raise GeminiError(f"Gemini API configuration failed: {e}", status_code=500)


# Use environment variable for model name if set, otherwise use config default
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
logger.info(f"Initializing Gemini model: {GEMINI_MODEL_NAME}")
gemini_model = None
try:
    gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    logger.info(f"Gemini model '{GEMINI_MODEL_NAME}' loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load Gemini model '{GEMINI_MODEL_NAME}': {e}. Check API key and model name.", exc_info=True)
    # Fallback could be attempted if applicable, or just raise
    # For now, if the primary model fails, we raise an error.
    raise GeminiError(f"Could not initialize Gemini model '{GEMINI_MODEL_NAME}': {e}", status_code=500)


def generate_insights(transcript: str) -> str:
    """
    Generates insights from a transcript using the configured Gemini model.
    """
    if not gemini_model:
        logger.error("Gemini model is not available or failed to load prior to insight generation.")
        raise GeminiError("Gemini model is not available or failed to load.", status_code=500)

    logger.info(f"Generating insights using Gemini model: {GEMINI_MODEL_NAME} for transcript of length {len(transcript)} chars.")
    logger.debug(f"Transcript snippet for Gemini: {transcript[:100]}...")

    prompt = f"""
Here is a meeting transcript:
{transcript}

Provide:
1. A short summary.
2. Action items with responsible people.
3. Sentiment of the overall meeting.
4. Key insights or decisions made during the meeting.
5. Number of participants.
6. Any follow-up questions or topics that need further discussion.
Please ensure the response is concise and structured.

Example response format:
Generating insights from Gemini...

✅ Gemini Output:

**1. Summary:** The meeting discussed YouTube's content recommendation algorithm.  The speaker argues that the algorithm reflects current global trends and individual user interests, aiming for diversity while prioritizing relevance.  A disagreement exists regarding the algorithm's transparency and control over content selection.

**2. Action Items:** None explicitly stated in the transcript.

**3. Sentiment:**  The overall sentiment is a mix of explanatory and slightly defensive regarding the YouTube algorithm.  There's an underlying tension between the algorithm's design goals and concerns about content control and transparency.

**4. Key Insights/Decisions:** No concrete decisions were made. The key insight is the speaker's perspective on the algorithm's design philosophy: prioritizing relevance and reflecting real-world trends over strict content selection.

**5. Number of Participants:**  The transcript indicates at least two participants,  one speaking and at least one listening ("you can choose an additive...").  The exact number is unknown.


**6. Follow-up Questions/Topics:**
* Clarification on the "additive" mentioned. What is it, and how does it relate to content creators seeing what should be shown?
* Deeper discussion on balancing diversity and relevance in the algorithm.
* Addressing concerns about the algorithm's lack of transparency and control for content creators.
* Exploring methods to improve the algorithm's responsiveness to user feedback.


Processed audio and generated insights.
**1. Summary:** The meeting discussed YouTube's content recommendation algorithm.  The speaker argues that the algorithm reflects current global trends and individual user interests, aiming for diversity while prioritizing relevance.  A disagreement exists regarding the algorithm's transparency and control over content selection.

**2. Action Items:** None explicitly stated in the transcript.

**3. Sentiment:**  The overall sentiment is a mix of explanatory and slightly defensive regarding the YouTube algorithm.  There's an underlying tension between the algorithm's design goals and concerns about content control and transparency.

**4. Key Insights/Decisions:** No concrete decisions were made. The key insight is the speaker's perspective on the algorithm's design philosophy: prioritizing relevance and reflecting real-world trends over strict content selection.

**5. Number of Participants:**  The transcript indicates at least two participants,  one speaking and at least one listening ("you can choose an additive...").  The exact number is unknown.

**6. Follow-up Questions/Topics:**
* Clarification on the "additive" mentioned. What is it, and how does it relate to content creators seeing what should be shown?
* Deeper discussion on balancing diversity and relevance in the algorithm.
* Addressing concerns about the algorithm's lack of transparency and control for content creators.
* Exploring methods to improve the algorithm's responsiveness to user feedback.

"""
    try:
        response = gemini_model.generate_content(prompt)
        logger.info("Gemini insights generated successfully.")
        logger.debug(f"Gemini response snippet: {response.text[:100]}...")
        return response.text
    except Exception as e:
        logger.error(f"Error during Gemini insight generation: {e}", exc_info=True)
        raise GeminiError(f"Gemini API call failed: {e}") # status_code defaults to 500
