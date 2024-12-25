from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from openai import AzureOpenAI
import base64
from dotenv import load_dotenv
import httpx
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Force reload of environment variables
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value.strip('"')

# Print environment variables for debugging
print("Environment variables:")
print(f"AZURE_OPENAI_KEY: {os.getenv('AZURE_OPENAI_KEY')[:10]}...")
print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION')}")
print(f"AZURE_OPENAI_GPT4O_DEPLOYMENT: {os.getenv('AZURE_OPENAI_GPT4O_DEPLOYMENT')}")

# Create a custom httpx client without proxies
http_client = httpx.Client(timeout=30.0)

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    http_client=http_client
)

class AzureVisionTool(BaseTool):
    """
    A tool for analyzing images using Azure OpenAI GPT-4 Omni capabilities.
    Can be used for general image analysis or specific tasks like OCR.
    """
    
    image_path: str = Field(
        ...,
        description="Path to the image file to analyze"
    )
    
    prompt: str = Field(
        default="What do you see in this image? Please describe the desktop contents in detail.",
        description="The prompt to send to GPT-4 Omni for image analysis"
    )
    
    mode: str = Field(
        default="analyze",
        description="Mode of operation: 'analyze' for general image analysis, 'ocr' for text extraction"
    )

    def run(self):
        """
        Analyzes the image using Azure OpenAI GPT-4 Omni and returns the description.
        For OCR mode, extracts and returns only the text from the image.
        """
        try:
            if not os.path.exists(self.image_path):
                print(f"Error: Image file not found at {self.image_path}")
                return None
                
            img = Image.open(self.image_path)
            # Convert image to base64 string
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Set the prompt based on mode
            if self.mode == "ocr":
                prompt = "Extract all text from this image. Return only the extracted text."
            else:
                prompt = self.prompt
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ]
            
            print("Sending request to Azure OpenAI...")
            print(f"Using deployment: {os.getenv('AZURE_OPENAI_GPT4O_DEPLOYMENT')}")
            
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),  # Use the deployment name from env
                messages=messages,
                max_tokens=4096
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    # Create test images directory
    test_dir = "vision_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a test image with text
    print("Creating test images...")
    
    # Text image for OCR testing
    text_image = Image.new('RGB', (800, 200), color='white')
    draw = ImageDraw.Draw(text_image)
    text = "Hello, this is a test of the OCR functionality!"
    font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (800 - text_width) // 2
    y = (200 - text_height) // 2
    draw.text((x, y), text, fill='black', font=font)
    text_image_path = os.path.join(test_dir, "text_test.png")
    text_image.save(text_image_path)
    
    # Visual image for analysis testing
    visual_image = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(visual_image)
    # Draw some shapes
    draw.rectangle([100, 100, 300, 300], outline='blue', width=2)
    draw.ellipse([400, 200, 600, 400], outline='red', width=2)
    draw.line([100, 500, 700, 500], fill='green', width=3)
    visual_image_path = os.path.join(test_dir, "visual_test.png")
    visual_image.save(visual_image_path)
    
    print("\nTesting AzureVisionTool...")
    
    # Test OCR
    print("\nTesting OCR mode...")
    tool = AzureVisionTool(
        image_path=text_image_path,
        mode="ocr"
    )
    result = tool.run()
    print(f"OCR result: {result}")
    
    # Test general analysis
    print("\nTesting analysis mode...")
    tool = AzureVisionTool(
        image_path=visual_image_path,
        prompt="Describe what you see in this image, including the shapes, colors, and their positions."
    )
    result = tool.run()
    print(f"Analysis result: {result}")
    
    # Clean up
    print("\nCleaning up test directory...")
    import shutil
    shutil.rmtree(test_dir) 