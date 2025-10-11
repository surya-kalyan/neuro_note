# NeuroNote - AI-Powered Meeting Insights

NeuroNote is a Flask-based web application that transcribes audio recordings and generates intelligent meeting insights using OpenAI Whisper and Google's Gemini AI.

## Features

- **Audio Transcription**: Convert meeting recordings to text using OpenAI Whisper
- **AI-Powered Analysis**: Generate summaries, action items, and insights using Google Gemini
- **Web Interface**: Simple HTML interface for uploading and processing audio files
- **RESTful API**: Easy integration with other applications

## Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd neuronote
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
DEBUG=True
```

### Running the Application

```bash
python neuronote.py
```

The application will start on `http://localhost:5000`

## Usage

1. Open the web interface at `http://localhost:5000`
2. Upload an audio file (WAV format recommended)
3. Wait for transcription and analysis
4. View the generated insights including:
   - Meeting summary
   - Action items
   - Sentiment analysis
   - Key insights
   - Participant count
   - Follow-up questions

## API Endpoints

### POST /recorded-audio
Upload audio file for processing

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Audio file with key 'file'

**Response:**
```json
{
  "status": "success",
  "text": "Generated meeting insights..."
}
```

## Project Structure

```
neuronote/
├── neuronote.py          # Main Flask application
├── test_neuronote.py     # Audio processing logic
├── analyzer.py           # Additional analysis utilities
├── transcriber.py        # Transcription utilities
├── templates/            # HTML templates
│   ├── index.html
│   ├── neuronote.html
│   └── style.css
├── static/               # Static files (empty)
├── uploads/              # Upload directory (empty)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.