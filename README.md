# Advanced Voice Recognition System

An advanced voice recognition system built using [Vosk](https://alphacephei.com/vosk/), designed for real-time speech-to-text transcription with support for various English dialects.

## Features

- 🎙️ Real-time continuous speech recognition  
- 🌎 Support for multiple English dialects  
- 📊 Confidence scoring for recognition results  
- 📝 Recognition history tracking  
- 🧱 Robust error handling and logging  
- 🔒 Thread-safe implementation  

## Prerequisites

- Python 3.7 or higher  
- A working microphone  
- At least 2GB of free disk space for the speech recognition model  

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Vosk Model

This project uses the `vosk-model-en-us-daanzu-20200905` model for high-accuracy English recognition.

- Visit the [Vosk Models Page](https://alphacephei.com/vosk/models)
- Scroll to the **"Other models"** section
- Download the **vosk-model-en-us-daanzu-20200905.zip**  
  Direct link: [Download Model](https://alphacephei.com/vosk/models/vosk-model-en-us-daanzu-20200905.zip)
- Extract the downloaded ZIP file
- Move the extracted folder (`vosk-model-en-us-daanzu-20200905`) into your project directory

## Usage

1. Ensure the model folder is in the project directory  
2. Run the system:

```bash
python voice_recognition.py
```

3. Start speaking. The system will:
   - Detect your voice  
   - Transcribe your speech  
   - Display text and confidence scores  
   - Log the recognition history  

4. Press `Ctrl + C` to stop the system  

## Advanced Configuration

You can customize recognition behavior by changing parameters in the `AdvancedVoiceRecognition` class:

- `model_path`: Path to the Vosk model directory  
- `sample_rate`: Audio sampling rate (default: `16000`)  
- `device`: Microphone device ID (default: `None` to use system default)  

## Troubleshooting

### Microphone Not Detected

- Ensure it’s plugged in correctly  
- Try a different device ID  
- Close other applications that might be using the microphone  

### Low Recognition Accuracy

- Move to a quiet environment  
- Speak clearly and naturally  
- Test with a different Vosk model if needed  

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
