from flask import Flask, request, render_template
from flask_cors import CORS
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_neuronote import process_audio

app = Flask(__name__, template_folder='../templates')
CORS(app)

@app.route('/')
def index():
    return render_template('neuronote.html')

@app.route('/recorded-audio', methods=['POST'])
def handle_audio():
    try:
        file = request.files['file']
        file_path = './meeting.wav'
        file.save(file_path)

        # Run transcription + Gemini analysis
        result = process_audio(file_path)
        print("Processed audio and generated insights.")
        print(f"[DEBUG] Gemini Output Length: {len(result)} characters")
        print(result)

        return {
            "status": "success",
            "text": result
        }
    except Exception as e:
        print(f"Error processing audio: {e}")
        return {
            "status": "error",
            "message": str(e)
        }, 500

# Vercel requires this
if __name__ == "__main__":
    app.run()