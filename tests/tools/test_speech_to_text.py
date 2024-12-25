from tools.SpeechToTextTool import SpeechToTextTool
import time
import json

def main():
    print("Testing Azure Speech-to-Text Tool...")
    
    # Test 1: Basic speech recognition
    print("\nTest 1: Quick speech recognition (5 seconds)")
    print("Please speak a brief sentence when prompted...")
    time.sleep(2)  # Give user time to prepare
    
    tool = SpeechToTextTool(
        duration_seconds=5,
        detailed_output=False
    )
    result = tool.run()
    print(f"\nBasic transcription result:\n{result}")
    
    time.sleep(2)  # Pause between tests
    
    # Test 2: Detailed output with timing
    print("\nTest 2: Detailed speech recognition (10 seconds)")
    print("Please speak a few sentences when prompted...")
    time.sleep(2)  # Give user time to prepare
    
    tool = SpeechToTextTool(
        duration_seconds=10,
        detailed_output=True
    )
    result = tool.run()
    if isinstance(result, dict):
        print("\nDetailed transcription result:")
        print(json.dumps(result, indent=2))
    else:
        print(f"\nResult: {result}")
    
    time.sleep(2)  # Pause between tests
    
    # Test 3: Longer conversation
    print("\nTest 3: Extended speech recognition (15 seconds)")
    print("Please speak continuously for a longer duration when prompted...")
    time.sleep(2)  # Give user time to prepare
    
    tool = SpeechToTextTool(
        duration_seconds=15,
        detailed_output=True
    )
    result = tool.run()
    if isinstance(result, dict):
        print("\nDetailed transcription result:")
        print(json.dumps(result, indent=2))
    else:
        print(f"\nResult: {result}")

if __name__ == "__main__":
    try:
        main()
        print("\nSpeech recognition tests completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nTest session ended.") 