# Transcription utilities for NeuroNote
import whisper

def load_whisper_model(model_size="base"):
    """Load Whisper model for transcription"""
    return whisper.load_model(model_size)

def transcribe_audio(model, audio_path):
    """Transcribe audio file using Whisper"""
    result = model.transcribe(audio_path)
    return result["text"]