import os
import whisper
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

api_key=os.getenv('GEMINI_API_KEY')

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
    gemini = genai.GenerativeModel('gemini-2.5-flash')


    # --- Prompt Creation ---
    prompt = f"""
    Here is a meeting transcript:
    {transcript}

    Provide:
    1. A short summary.
    2. Action items with responsible people.
    3. Sentiment of the overall meeting.
    4. Key insights of the meeting.
    5. Number of participants.
    6. Any follow-up questions.
    Please ensure the response is concise and structured.

    Example format:
    Gemini Output:

**1. Summary:** This meeting transcript captures a discussion about Google's transition to AI-driven products, specifically focusing on the evolution of Google Search.  Concerns about the impact of generative AI on search quality, competition, and user experience are addressed, along with the challenges of maintaining accuracy and combating misinformation in a rapidly changing landscape. The discussion also touches on Google's internal culture and the company's overall direction.

**2. Action Items:**  None explicitly stated. The conversation is primarily a brainstorming session and internal reflection on strategic direction.

**3. Sentiment:** A mix of cautious optimism and concern. While excited about the potential of AI, there's a palpable awareness of the significant challenges and risks involved in this transition.  There's also a sense of urgency and a recognition of the need to adapt quickly.

**4. Key Insights:**
* **AI-driven Search Evolution:** Google is actively integrating generative AI into Search, aiming to provide more direct answers while maintaining the importance of linked sources.

* **Quality Control Challenges:**  The shift to AI presents challenges regarding accuracy, combating misinformation (spam, biased results), and maintaining user trust.

* **Global Implications:** The impact of AI-powered Search needs to be considered on a global scale, addressing diverse queries and cultural contexts.

* **Competitive Landscape:** The conversation acknowledges the competitive pressure and potential threats to Google's market dominance.

* **Internal Culture:** The meeting touches on Google's internal culture, its strengths (transparency, employee voice) and potential areas for improvement.

**5. Number of Participants:** The number of participants is maybe one/two. it looks like a two-person conversation, likely between a Google executive and a senior engineer or product manager.

**6. Follow-up Questions:**
* What specific metrics will be used to measure the success of the AI integration into Search?
* What strategies are in place to mitigate the risks associated with AI-generated misinformation and bias?
* How will Google address concerns from publishers and competitors regarding the changes to Search?
* What specific steps are being taken to adapt Google's internal culture to support this significant technological shift?
    """

    # --- Generate Insights ---
    print("Generating insights from Gemini...")
    response = gemini.generate_content(prompt)
    print("\nGemini Output:\n")
    # Handle encoding issues
    try:
        print(response.text.encode('utf-8', errors='ignore').decode('utf-8'))
        return response.text
    except UnicodeEncodeError:
        clean_text = response.text.encode('ascii', errors='ignore').decode('ascii')
        print(clean_text)
        return clean_text

# if __name__ == "__main__":
