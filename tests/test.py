from DesktopVisionAgent import DesktopVisionAgent

def main():
    # Create an instance of the agent
    agent = DesktopVisionAgent()
    
    # Test screenshot analysis
    print("\nTesting screenshot analysis:")
    result = agent.analyze_desktop("What applications and windows do you see on my desktop?")
    print(f"Analysis result: {result}")
    
    # Test chat
    print("\nTesting chat:")
    chat_result = agent.chat("What can you help me with regarding my desktop?")
    print(f"Chat response: {chat_result}")

if __name__ == "__main__":
    main() 