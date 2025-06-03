import os
import whisper
import google.generativeai as genai

api_key="AIzaSyB32ovJDzjRfVsXSHMB6DzPd33iGfA7tBM"

# --- Whisper Setup ---
model = whisper.load_model("base")

# Provide the correct full path to your audio file


def process_audio(file_path):
    print("Transcribing audio...")
    result = model.transcribe(file_path)
    transcript = result["text"]

    # --- Gemini Setup ---
    # api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    gemini = genai.GenerativeModel('models/gemini-1.5-flash-latest')


    # --- Prompt Creation ---
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
    """

    # --- Generate Insights ---
    print("Generating insights from Gemini...")
    response = gemini.generate_content(prompt)
    print("\n✅ Gemini Output:\n")
    print(response.text)
    return response.text

# if __name__ == "__main__":
