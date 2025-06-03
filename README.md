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
pip install flask flask-cors google-generativeai whisper
# Ensure ffmpeg is installed for Whisper:
# sudo apt update && sudo apt install ffmpeg
```

---

### 🚀 Running the Development Server

To run the application with Flask's built-in development server:

```bash
python neuronote.py
```

By default, it runs on:

```
http://localhost:5000
```
(or as configured by `FLASK_RUN_HOST`/`FLASK_RUN_PORT` environment variables).

Make sure necessary environment variables like `GEMINI_API_KEY` are set.

---

### 🎯 API Endpoint

#### POST `/recorded-audio`

Uploads an audio file (e.g., `.wav`, `.mp3`) and returns AI-generated insights.

##### Request:

* `multipart/form-data` with field:

  * `file`: the audio recording

##### Example with `curl`:

```bash
curl -X POST http://localhost:5000/recorded-audio \
  -F "file=@path/to/your/meeting_audio.wav"
```

##### Response:

```json
{
  "status": "success",
  "text": "1. A short summary...\n2. Action items...\n..."
}
```
Or in case of an error (example):
```json
{
  "status": "error",
  "message": "Error during audio transcription."
}
```

---

### ⚙️ Configuration

The application can be configured via `config.py` and environment variables. Key environment variables include:

*   `GEMINI_API_KEY`: Your API key for the Gemini service. **(Required)**
*   `LOG_LEVEL`: Sets the application's log level (e.g., `INFO`, `DEBUG`, `WARNING`). Defaults to `INFO`.
*   `ENABLE_FILE_LOGGING`: Set to `true` to enable logging to `app.log`. Defaults to `false`.
*   `FLASK_DEBUG`: Set to `true` or `false` to override the debug mode from `config.py`.
*   `WHISPER_MODEL`: Name of the Whisper model to use (e.g., `base`, `small`, `medium`). Defaults to `base`.
*   `GEMINI_MODEL`: Name of the Gemini model to use. Defaults to `models/gemini-1.5-flash-latest`.
*   `FLASK_RUN_HOST`: Host for the development server. Defaults to `0.0.0.0`.
*   `FLASK_RUN_PORT`: Port for the development server. Defaults to `5000`.

---

### 📁 Project Structure

```
.
├── neuronote.py          # Main Flask application file
├── wsgi.py               # WSGI entry point for Gunicorn
├── config.py             # Default configuration settings
├── services/             # Business logic modules
│   ├── __init__.py
│   ├── transcription.py  # Handles audio transcription
│   └── gemini.py         # Handles Gemini AI interactions
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── error_handlers.py # Custom error classes and Flask error handlers
│   └── logger.py         # Logging configuration
├── app.log               # Log file (if file logging is enabled)
└── README.md             # This file
```
(Note: `meeting.wav` is a temporary file created during upload.)

---

## 🦄 Running in Production (with Gunicorn)

To run the NeuroNote application using a production-ready WSGI server like Gunicorn, follow these steps:

1.  **Install Gunicorn:**
    ```bash
    pip install gunicorn
    ```

2.  **Run the application using Gunicorn:**
    Navigate to the project's root directory (where `wsgi.py` and `neuronote.py` are located) and run:
    ```bash
    gunicorn --bind 0.0.0.0:5000 wsgi:app
    ```
    *   `--bind 0.0.0.0:5000`: This tells Gunicorn to listen on all network interfaces on port 5000. You can change the port as needed (or use the `PORT` environment variable if your PaaS sets it).
    *   `wsgi:app`: This tells Gunicorn to look for a file named `wsgi.py` and use the Flask application instance named `app` from it.

3.  **Configuration (Recommended):**
    For more advanced Gunicorn configurations (e.g., number of workers, timeout settings, logging), you can use a Gunicorn configuration file or command-line arguments. Refer to the [Gunicorn documentation](https://docs.gunicorn.org/en/stable/settings.html) for details.

    Example with more workers (a common starting point is `(2 x $num_cores) + 1`):
    ```bash
    gunicorn -w 4 --bind 0.0.0.0:5000 wsgi:app
    ```
    (`-w` specifies the number of worker processes)

4.  **Environment Variables:**
    Ensure all necessary environment variables (e.g., `GEMINI_API_KEY`, `LOG_LEVEL`, `ENABLE_FILE_LOGGING`, `FLASK_DEBUG` (should be `false` in prod), `WHISPER_MODEL`, `GEMINI_MODEL`) are set in the environment where Gunicorn is running. These variables are crucial for the application to function correctly. For example, `GEMINI_API_KEY` must be provided.

---
