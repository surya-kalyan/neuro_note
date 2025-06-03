from flask import Flask, request
from flask_cors import CORS
import os
from test_neuronote import process_audio  # we'll extract this from your existing code

app = Flask(__name__)
CORS(app)

@app.route('/recorded-audio', methods=['POST'])
def handle_audio():
    file = request.files['file']
    file_path = './meeting.wav'
    file.save(file_path)

    # Run transcription + Gemini analysis
    result = process_audio(file_path)
    print("Processed audio and generated insights.")
    print(result)
    try:
        return {
            "status" : "success",
            "text" : result
        }
    except Exception as e:
        print(f"Error processing audio: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    app.run(debug=True)
# test_neuronote.py