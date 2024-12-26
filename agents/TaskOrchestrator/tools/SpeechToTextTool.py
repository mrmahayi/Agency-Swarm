from agency_swarm.tools import BaseTool
from pydantic import Field
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, ResultReason, CancellationDetails, CancellationReason, audio, ServicePropertyChannel
import os
from dotenv import load_dotenv
import time

load_dotenv()

class SpeechToTextTool(BaseTool):
    """
    A tool for converting speech to text using Azure's Speech-to-Text service.
    Supports continuous speech recognition and provides real-time transcription.
    """
    
    duration: int = Field(
        default=10,
        description="The duration in seconds to listen for speech input"
    )
    
    language: str = Field(
        default="en-US",
        description="The language code for speech recognition. Default is US English."
    )

    def run(self):
        """
        Listens for speech input and converts it to text using Azure's Speech-to-Text service.
        Returns the transcribed text if successful.
        """
        # Get Azure Speech credentials from environment variables
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_SPEECH_REGION")
        endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
        api_version = os.getenv("AZURE_SPEECH_API_VERSION")
        
        if not all([speech_key, service_region, endpoint, api_version]):
            missing = [var for var, val in {
                "AZURE_SPEECH_KEY": speech_key,
                "AZURE_SPEECH_REGION": service_region,
                "AZURE_SPEECH_ENDPOINT": endpoint,
                "AZURE_SPEECH_API_VERSION": api_version
            }.items() if not val]
            return f"Error: Missing environment variables: {', '.join(missing)}"
        
        try:
            # Configure speech service
            speech_config = SpeechConfig(
                subscription=speech_key, 
                region=service_region
            )
            
            # Set the endpoint URL
            endpoint_url = f"{endpoint}?api-version={api_version}"
            print(f"Using endpoint URL: {endpoint_url}")
            
            speech_config.set_service_property(
                name="endpoint",
                value=endpoint_url,
                channel=ServicePropertyChannel.UriQueryParameter
            )
            
            speech_config.speech_recognition_language = self.language
            print(f"Using language: {self.language}")
            
            # Create speech recognizer with default microphone input
            audio_config = audio.AudioConfig(use_default_microphone=True)
            speech_recognizer = SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            print(f"Listening for {self.duration} seconds...")
            result = speech_recognizer.recognize_once_async().get()
            
            if result.reason == ResultReason.RecognizedSpeech:
                return f"Recognized text: {result.text}"
            elif result.reason == ResultReason.NoMatch:
                return "No speech could be recognized"
            elif result.reason == ResultReason.Canceled:
                cancellation_details = CancellationDetails(result)
                if cancellation_details.reason == CancellationReason.Error:
                    return f"Speech recognition canceled due to error. Error details: {cancellation_details.error_details}"
                else:
                    return f"Speech recognition canceled. Reason: {cancellation_details.reason}"
            else:
                return f"Error recognizing speech: {result.reason}"
                
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the speech-to-text tool
    tool = SpeechToTextTool(
        duration=5,
        language="en-US"
    )
    print(tool.run()) 