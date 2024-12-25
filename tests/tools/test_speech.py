from tools.SpeechTool import SpeechTool
import time

def main():
    print("Testing Azure Text-to-Speech Tool with Jenny's voice...")
    
    # Test 1: Simple greeting
    print("\nTest 1: Simple greeting")
    tool = SpeechTool(
        text="Hello! I'm Jenny, your virtual assistant. How can I help you today?",
        voice_name="en-US-JennyNeural"
    )
    print(tool.run())
    time.sleep(3)  # Wait for speech to complete
    
    # Test 2: Professional announcement
    print("\nTest 2: Professional announcement")
    tool = SpeechTool(
        text="Welcome to our presentation. Today, we'll be discussing the latest developments in artificial intelligence and machine learning.",
        voice_name="en-US-JennyNeural"
    )
    print(tool.run())
    time.sleep(3)  # Wait for speech to complete
    
    # Test 3: Longer conversational text
    print("\nTest 3: Longer conversational text")
    long_text = """
    I'd love to tell you about what I can do. I can help with reading text aloud, 
    making announcements, or providing voice responses in a natural, conversational way. 
    My voice is designed to be clear, professional, and easy to understand. 
    Would you like to try out any specific type of text?
    """
    tool = SpeechTool(
        text=long_text,
        voice_name="en-US-JennyNeural"
    )
    print(tool.run())

if __name__ == "__main__":
    main() 