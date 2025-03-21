# Advanced Voice Recognition System

This is an advanced voice recognition system built using Vosk, capable of understanding multiple English dialects with high accuracy.

## Features

- Real-time continuous speech recognition
- Support for multiple English dialects
- Confidence scoring for recognition results
- Recognition history tracking
- Robust error handling and logging
- Thread-safe implementation

## Prerequisites

- Python 3.7 or higher
- A working microphone
- Sufficient disk space for the Vosk model (approximately 2GB)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Download the Vosk model:
   - Visit https://alphacephei.com/vosk/models
   - Download the desired English model (recommended: vosk-model-en-us-0.42)
   - Extract the model to your project directory

## Usage

1. Make sure the Vosk model is in your project directory
2. Run the voice recognition system:
```bash
python voice_recognition.py
```

3. Start speaking - the system will automatically:
   - Detect and transcribe your speech
   - Display the recognized text
   - Show confidence scores for the recognition
   - Store the recognition history

4. Press Ctrl+C to stop the recognition

## Advanced Configuration

You can customize the voice recognition by modifying the following parameters when initializing the `AdvancedVoiceRecognition` class:

- `model_path`: Path to a different Vosk model
- `sample_rate`: Audio sample rate (default: 16000)
- `device`: Specific audio device ID (default: None, uses system default)

## Troubleshooting

1. If you encounter audio device issues:
   - Check if your microphone is properly connected
   - Try specifying a different audio device ID
   - Ensure no other application is using the microphone

2. If recognition accuracy is low:
   - Try using a different Vosk model
   - Ensure you're in a quiet environment
   - Speak clearly and at a moderate pace

## License

This project is open source and available under the MIT License. 
