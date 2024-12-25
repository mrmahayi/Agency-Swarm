from agency_swarm.tools import BaseTool
from pydantic import Field
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import time

load_dotenv()

class SpeechTool(BaseTool):
    """
    A tool for converting text to speech using Azure's Text-to-Speech service.
    Supports multiple voices and provides natural-sounding speech synthesis.
    """
    
    text: str = Field(
        ..., 
        description="The text to be converted to speech"
    )
    
    voice_name: str = Field(
        default="en-US-JennyNeural",
        description="The name of the voice to use for speech synthesis. Default is Jenny (female). Other options include en-US-GuyNeural (male)"
    )

    def run(self):
        """
        Converts the provided text to speech using Azure's Text-to-Speech service.
        Returns a success message if the speech was synthesized successfully.
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
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key, 
                region=service_region
            )
            
            # Set the endpoint URL
            endpoint_url = f"{endpoint}?api-version={api_version}"
            print(f"Using endpoint URL: {endpoint_url}")
            
            speech_config.set_service_property(
                name="endpoint",
                value=endpoint_url,
                channel=speechsdk.ServicePropertyChannel.UriQueryParameter
            )
            
            speech_config.speech_synthesis_voice_name = self.voice_name
            print(f"Using voice: {self.voice_name}")
            
            # Create speech synthesizer with default speaker output
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            # Synthesize text to speech
            result = speech_synthesizer.speak_text_async(self.text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return f"Successfully synthesized speech for text: {self.text[:50]}..."
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speechsdk.CancellationDetails(result)
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    return f"Speech synthesis canceled due to error. Error details: {cancellation_details.error_details}"
                else:
                    return f"Speech synthesis canceled. Reason: {cancellation_details.reason}"
            else:
                return f"Error synthesizing speech: {result.reason}"
                
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the speech tool
    tool = SpeechTool(
        text="Hello! This is a test of the Azure Text-to-Speech service.",
        voice_name="en-US-JennyNeural"
    )
    print(tool.run())
    
    time.sleep(2)  # Wait for first speech to complete
    
    # Test with different voice
    tool = SpeechTool(
        text="Now I'm speaking with a different voice.",
        voice_name="en-US-GuyNeural"
    )
    print(tool.run()) 