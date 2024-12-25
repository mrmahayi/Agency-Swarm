from agency_swarm.tools import BaseTool
from pydantic import Field
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import time
from typing import List, Dict

load_dotenv()

class SpeechToTextTool(BaseTool):
    """
    A tool for converting English speech to text using Azure's Speech Service with Whisper model.
    Supports continuous speech recognition and can transcribe audio in real-time.
    """
    
    duration_seconds: int = Field(
        default=10,
        description="Duration in seconds to listen for speech input. Default is 10 seconds."
    )
    
    detailed_output: bool = Field(
        default=False,
        description="If True, returns detailed information including timing and recognition segments."
    )

    def run(self):
        """
        Listens for English speech input and converts it to text using Azure's Speech Service.
        Returns the transcribed text and optional detailed information.
        """
        # Get Azure Speech credentials from environment variables
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_SPEECH_REGION")
        endpoint = os.getenv("AZURE_WHISPER_ENDPOINT")
        api_version = os.getenv("AZURE_WHISPER_API_VERSION")
        
        if not all([speech_key, service_region, endpoint, api_version]):
            missing = [var for var, val in {
                "AZURE_SPEECH_KEY": speech_key,
                "AZURE_SPEECH_REGION": service_region,
                "AZURE_WHISPER_ENDPOINT": endpoint,
                "AZURE_WHISPER_API_VERSION": api_version
            }.items() if not val]
            return f"Error: Missing environment variables: {', '.join(missing)}"
        
        try:
            # Configure speech service
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key, 
                region=service_region
            )
            
            # Set the endpoint URL for Whisper model
            endpoint_url = f"{endpoint}?api-version={api_version}"
            print(f"Using endpoint URL: {endpoint_url}")
            
            speech_config.set_service_property(
                name="endpoint",
                value=endpoint_url,
                channel=speechsdk.ServicePropertyChannel.UriQueryParameter
            )
            
            # Set to English
            speech_config.speech_recognition_language = "en-US"
            print("Using English (US) recognition")
            
            # Create speech recognizer with default microphone input
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            print(f"\nListening for {self.duration_seconds} seconds...")
            
            # Store the transcribed text and details
            recognition_results = []
            
            # Callback to handle recognized speech
            def handle_result(evt):
                if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    result_dict = {
                        "text": evt.result.text,
                        "offset": evt.result.offset,
                        "duration": evt.result.duration
                    }
                    recognition_results.append(result_dict)
                    print(f"Recognized: {evt.result.text}")
            
            # Handle errors
            def handle_error(evt):
                print(f'Error: {evt.result.error_details}')
            
            # Subscribe to events
            speech_recognizer.recognized.connect(handle_result)
            speech_recognizer.canceled.connect(handle_error)
            
            # Start continuous recognition
            speech_recognizer.start_continuous_recognition()
            time.sleep(self.duration_seconds)  # Listen for specified duration
            speech_recognizer.stop_continuous_recognition()
            
            if not recognition_results:
                return "No speech detected during the listening period."
            
            if self.detailed_output:
                return {
                    "results": recognition_results,
                    "duration": self.duration_seconds,
                    "total_segments": len(recognition_results)
                }
            else:
                return "\n".join([r["text"] for r in recognition_results])
                
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the speech-to-text tool
    print("Testing English Speech-to-Text conversion...")
    print("Please speak into your microphone when prompted.")
    
    tool = SpeechToTextTool(
        duration_seconds=5,  # Listen for 5 seconds
        detailed_output=True  # Get detailed results
    )
    result = tool.run()
    print(f"\nTranscription result:\n{result}") 