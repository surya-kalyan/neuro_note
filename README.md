## 🧠 NeuroNote 

Flask-based backend for **NeuroNote**, a meeting insights assistant that:

* Accepts audio recordings via a POST API.
* Transcribes and analyzes them using the Gemini API (via `test_neuronote.py`).
* Returns structured meeting summaries, action items, and more.

---

### 🔧 Requirements

Make sure you have the following installed:

```bash
python>=3.8
```

Install dependencies:

```bash
pip install flask flask-cors
# plus whatever is needed by test_neuronote.py
```

---

### 🚀 Running the Server

```bash
python neuronote.py
```

By default, it runs on:

```
http://localhost:5000
```

---

### 🎯 API Endpoint

#### POST `/recorded-audio`

Uploads a `.wav` audio file and returns AI-generated insights.

##### Request:

* `multipart/form-data` with field:

  * `file`: the `.wav` audio recording

##### Example with `curl`:

```bash
curl -X POST http://localhost:5000/recorded-audio \
  -F "file=@meeting.wav"
```

##### Response:

```json
{
  "status": "success",
  "text": "**1. Summary:** The meeting discussed..."
}
```

---

### 🧠 Gemini Processing

The audio file is passed to `process_audio()` from `test_neuronote.py`, which is responsible for:

* Transcribing the `.wav` file.
* Sending the transcript to Gemini API.
* Structuring the insights as Markdown.

---

### 📁 File Structure

```bash
.
├── neuronote.py          # Flask server
├── test_neuronote.py     # Gemini + transcription logic
└── meeting.wav           # Temporary file for uploaded audio
├── templates/
│   └── index.html          # Frontend UI (recording, playback, results)
│   └── styles.css
```

---

