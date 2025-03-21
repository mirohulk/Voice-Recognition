import sys
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import threading
import time
from typing import Optional, Dict, List
import logging
import os
from vosk import SetLogLevel
import urllib.request
import zipfile

class AdvancedVoiceRecognition:
    def __init__(self, model_path: str = "vosk-model-en-us-daanzu-20200905", 
                 sample_rate: int = 16000,
                 device: Optional[int] = None):
        """
        Initialize the voice recognition system.
        
        Args:
            model_path: Path to the Vosk model
            sample_rate: Audio sample rate
            device: Audio device ID (None for default)
        """
        self.sample_rate = sample_rate
        self.device = device
        self.q = queue.Queue()
        self.running = False
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Suppress Vosk logging
        SetLogLevel(-1)
        
        # Check if model exists, if not download it
        if not os.path.exists(model_path):
            self.download_model(model_path)
        
        try:
            self.model = Model(model_path)
            self.logger.info(f"Loaded model from {model_path}")
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            raise
            
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.recognizer.SetWords(True)  # Enable word timing
        
        # Store recognition history
        self.recognition_history: List[Dict] = []
        
        # Symbol mappings
        self.symbol_mappings = {
            "dash": "-",
            "hyphen": "-",
            "minus": "-"
        }
    
    def process_text(self, text: str) -> str:
        """Process recognized text to convert words to symbols"""
        words = text.split()
        processed_words = []
        
        for word in words:
            # Convert word to lowercase for matching
            lower_word = word.lower()
            # Replace with symbol if it exists in mappings
            processed_word = self.symbol_mappings.get(lower_word, word)
            processed_words.append(processed_word)
        
        return " ".join(processed_words)
    
    def download_model(self, model_name: str):
        """Download and extract the Vosk model"""
        self.logger.info(f"Downloading model {model_name}...")
        model_url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
        zip_path = f"{model_name}.zip"
        
        try:
            # Download the model
            urllib.request.urlretrieve(model_url, zip_path)
            
            # Extract the model
            self.logger.info("Extracting model...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('.')
            
            # Clean up the zip file
            os.remove(zip_path)
            self.logger.info("Model downloaded and extracted successfully")
        except Exception as e:
            self.logger.error(f"Failed to download model: {str(e)}")
            raise
        
    def callback(self, indata, frames, time, status):
        """Callback for audio stream processing"""
        if status:
            self.logger.warning(f"Audio callback status: {status}")
        self.q.put(bytes(indata))
        
    def process_audio_chunk(self, audio_chunk) -> Optional[Dict]:
        """Process a chunk of audio data and return recognition results"""
        if self.recognizer.AcceptWaveform(audio_chunk):
            result = json.loads(self.recognizer.Result())
            if result.get("text"):
                # Process text to convert words to symbols
                result["text"] = self.process_text(result["text"])
                return result
        return None
        
    def start_recognition(self):
        """Start continuous voice recognition"""
        self.running = True
        
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                device=self.device,
                dtype="int16",
                channels=1,
                callback=self.callback
            ):
                self.logger.info("Started listening... Speak now! (Say 'dash' for -)")
                
                while self.running:
                    try:
                        audio_chunk = self.q.get()
                        result = self.process_audio_chunk(audio_chunk)
                        
                        if result:
                            self.recognition_history.append(result)
                            
                            # Print recognition results with confidence scores and timing
                            text = result["text"]
                            if "result" in result:
                                # Calculate overall confidence
                                conf = sum(word.get("conf", 0) for word in result["result"]) / len(result["result"])
                                
                                # Get timing information
                                start_time = result["result"][0].get("start", 0)
                                end_time = result["result"][-1].get("end", 0)
                                
                                self.logger.info(f"Recognized [{start_time:.2f}s - {end_time:.2f}s]: {text}")
                                self.logger.info(f"Confidence: {conf:.2f}")
                                
                                # Log detailed word information
                                for word in result["result"]:
                                    word_conf = word.get("conf", 0)
                                    if word_conf < 0.8:
                                        self.logger.debug(
                                            f"Word: {word['word']:<20} "
                                            f"Confidence: {word_conf:.2f} "
                                            f"Time: [{word.get('start', 0):.2f}s - {word.get('end', 0):.2f}s]"
                                        )
                            else:
                                self.logger.info(f"Recognized: {text}")
                                
                    except queue.Empty:
                        continue
                        
        except Exception as e:
            self.logger.error(f"Error in recognition: {str(e)}")
            self.stop_recognition()
            
    def stop_recognition(self):
        """Stop the voice recognition"""
        self.running = False
        self.logger.info("Stopping voice recognition...")
        
    def get_recognition_history(self) -> List[Dict]:
        """Return the history of recognized speech"""
        return self.recognition_history
        
    def clear_history(self):
        """Clear the recognition history"""
        self.recognition_history.clear()
        
def main():
    try:
        recognizer = AdvancedVoiceRecognition()
    except Exception as e:
        logging.error(f"Failed to initialize voice recognition: {str(e)}")
        sys.exit(1)
        
    try:
        # Start recognition in a separate thread
        recognition_thread = threading.Thread(target=recognizer.start_recognition)
        recognition_thread.start()
        
        # Keep the main thread running and handle user input
        print("Press Ctrl+C to stop recognition")
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        recognizer.stop_recognition()
        recognition_thread.join()
        
        # Print final statistics
        history = recognizer.get_recognition_history()
        print(f"\nRecognition session completed.")
        print(f"Total utterances recognized: {len(history)}")
        
if __name__ == "__main__":
    main() 