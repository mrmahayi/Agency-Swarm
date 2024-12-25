import os
from agency_swarm import Agent
from tools.AzureVisionTool import AzureVisionTool
from tools.CommunicationTool import CommunicationTool
from tools.TaskManagementTool import TaskManagementTool
from tools.MessageAnalyticsTool import MessageAnalyticsTool
from tools.VisualizationTool import VisualizationTool
import json
from datetime import datetime

class VisionAnalysisAgent(Agent):
    """
    Agent responsible for vision analysis and image processing tasks.
    """
    def __init__(self):
        super().__init__(
            name="VisionAnalysis",
            description="Processes and analyzes visual content",
            instructions="./instructions.md",
            tools=[
                AzureVisionTool,
                CommunicationTool,
                TaskManagementTool,
                MessageAnalyticsTool,
                VisualizationTool
            ],
            model=os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT"),
            temperature=0.7,
            max_prompt_tokens=25000
        )
        
        # Initialize state
        self.current_task = None
        self.vision_context = {}
        self.conversation_history = []
    
    def chat(self, message: str) -> str:
        """
        Process incoming chat messages and return appropriate responses.
        Analyzes message intent and performs necessary vision analysis tasks.
        """
        try:
            # Add message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Analyze message intent
            message_tool = MessageAnalyticsTool(
                message=message,
                operation="analyze_intent"
            )
            intents = json.loads(message_tool.run())
            
            # Extract entities from message
            entity_tool = MessageAnalyticsTool(
                message=message,
                operation="extract_entities"
            )
            entities = json.loads(entity_tool.run())
            
            # Process message based on intent
            response = self._process_intents(intents, entities, message)
            
            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.conversation_history.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().isoformat(),
                "error": True
            })
            return error_msg
    
    def _process_intents(self, intents: list, entities: dict, message: str) -> str:
        """Process message intents and generate appropriate response."""
        try:
            # Handle image analysis
            if any(intent in intents for intent in ["analyze", "examine", "describe"]):
                return self._handle_image_analysis(message, entities)
            
            # Handle OCR
            elif any(intent in intents for intent in ["ocr", "text", "read"]):
                return self._handle_ocr(message, entities)
            
            # Handle object detection
            elif any(intent in intents for intent in ["detect", "find", "locate"]):
                return self._handle_object_detection(message, entities)
            
            # Handle visualization
            elif any(intent in intents for intent in ["visualize", "plot", "graph"]):
                return self._handle_visualization(message, entities)
            
            # Handle help request
            elif "help" in message.lower():
                return self._handle_help_request()
            
            else:
                return (
                    "I can help you with vision analysis tasks like:\n"
                    "- Analyzing images\n"
                    "- Extracting text (OCR)\n"
                    "- Detecting objects\n"
                    "- Creating visualizations\n\n"
                    "What would you like me to analyze?"
                )
        
        except Exception as e:
            return f"Error processing intents: {str(e)}"
    
    def _handle_image_analysis(self, message: str, entities: dict) -> str:
        """Handle image analysis requests."""
        try:
            # Extract image path from entities or message
            image_path = entities.get("image_path")
            if not image_path:
                # Look for path patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'image\s*=\s*([^\s]+)',
                    r'analyze\s+([^\s]+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        image_path = match.group(1)
                        break
            
            if not image_path:
                return "Could not determine image to analyze"
            
            # Analyze image using AzureVisionTool
            vision_tool = AzureVisionTool(
                operation="analyze",
                image_path=image_path
            )
            result = json.loads(vision_tool.run())
            
            # Update vision context
            self.vision_context["analysis"] = {
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path,
                "result": result
            }
            
            # Format analysis results
            analysis = "Image Analysis Results:\n\n"
            
            if "description" in result:
                analysis += f"Description: {result['description']}\n\n"
            
            if "tags" in result:
                analysis += "Tags:\n"
                for tag in result["tags"]:
                    analysis += f"- {tag}\n"
                analysis += "\n"
            
            if "objects" in result:
                analysis += "Objects Detected:\n"
                for obj in result["objects"]:
                    analysis += f"- {obj['object']} ({obj['confidence']:.2%})\n"
                analysis += "\n"
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def _handle_ocr(self, message: str, entities: dict) -> str:
        """Handle OCR requests."""
        try:
            # Extract image path from entities or message
            image_path = entities.get("image_path")
            if not image_path:
                # Look for path patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'image\s*=\s*([^\s]+)',
                    r'read\s+([^\s]+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        image_path = match.group(1)
                        break
            
            if not image_path:
                return "Could not determine image for OCR"
            
            # Perform OCR using AzureVisionTool
            vision_tool = AzureVisionTool(
                operation="ocr",
                image_path=image_path
            )
            result = json.loads(vision_tool.run())
            
            # Update vision context
            self.vision_context["ocr"] = {
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path,
                "result": result
            }
            
            # Format OCR results
            if not result.get("text"):
                return "No text detected in the image"
            
            ocr_text = "Extracted Text:\n\n"
            ocr_text += result["text"]
            
            return ocr_text
            
        except Exception as e:
            return f"Error performing OCR: {str(e)}"
    
    def _handle_object_detection(self, message: str, entities: dict) -> str:
        """Handle object detection requests."""
        try:
            # Extract image path and target object from entities or message
            image_path = entities.get("image_path")
            target_object = entities.get("object")
            
            if not image_path:
                # Look for path patterns
                import re
                patterns = [
                    r'"([^"]+)"',
                    r'image\s*=\s*([^\s]+)',
                    r'in\s+([^\s]+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, message)
                    if match:
                        image_path = match.group(1)
                        break
            
            if not image_path:
                return "Could not determine image for object detection"
            
            # Detect objects using AzureVisionTool
            vision_tool = AzureVisionTool(
                operation="detect_objects",
                image_path=image_path
            )
            result = json.loads(vision_tool.run())
            
            # Update vision context
            self.vision_context["detection"] = {
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path,
                "target_object": target_object,
                "result": result
            }
            
            # Format detection results
            if not result.get("objects"):
                return "No objects detected in the image"
            
            detection = "Object Detection Results:\n\n"
            
            if target_object:
                # Filter for specific object
                matching_objects = [
                    obj for obj in result["objects"]
                    if target_object.lower() in obj["object"].lower()
                ]
                
                if not matching_objects:
                    return f"No {target_object} found in the image"
                
                detection += f"Found {len(matching_objects)} {target_object}(s):\n"
                for obj in matching_objects:
                    detection += f"- Confidence: {obj['confidence']:.2%}\n"
                    detection += f"  Location: {obj['location']}\n"
            else:
                # List all objects
                detection += f"Found {len(result['objects'])} objects:\n"
                for obj in result["objects"]:
                    detection += f"- {obj['object']} ({obj['confidence']:.2%})\n"
            
            return detection
            
        except Exception as e:
            return f"Error detecting objects: {str(e)}"
    
    def _handle_visualization(self, message: str, entities: dict) -> str:
        """Handle visualization requests."""
        try:
            # Check if we have data to visualize
            if not self.vision_context:
                return "No vision analysis data available for visualization"
            
            # Determine visualization type
            viz_type = None
            if "detection" in self.vision_context:
                viz_type = "object_detection"
            elif "analysis" in self.vision_context:
                viz_type = "analysis"
            elif "ocr" in self.vision_context:
                viz_type = "ocr"
            
            if not viz_type:
                return "No suitable data found for visualization"
            
            # Create visualization using VisualizationTool
            viz_tool = VisualizationTool(
                operation="create",
                data=self.vision_context[viz_type]["result"],
                viz_type=viz_type,
                output_path=f"visualizations/vision_{viz_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            result = viz_tool.run()
            
            # Update vision context
            self.vision_context["visualization"] = {
                "timestamp": datetime.now().isoformat(),
                "type": viz_type,
                "result": result
            }
            
            return f"Generated visualization: {result}"
            
        except Exception as e:
            return f"Error creating visualization: {str(e)}"
    
    def _handle_help_request(self) -> str:
        """Handle help requests."""
        return """
Available commands:
- Analyze: "Analyze image [path]" or "Describe image [path]"
- OCR: "Extract text from [path]" or "Read text in [path]"
- Detect: "Detect objects in [path]" or "Find [object] in [path]"
- Visualize: "Visualize results" or "Create visualization"

Examples:
- "Analyze image 'photo.jpg'"
- "Extract text from 'document.png'"
- "Find cars in 'street.jpg'"
- "Visualize the detection results"
"""

if __name__ == "__main__":
    # Test the VisionAnalysisAgent
    agent = VisionAnalysisAgent()
    
    print("Testing VisionAnalysisAgent...")
    
    # Test image analysis
    print("\nTesting image analysis:")
    response = agent.chat('Analyze image "test_image.jpg"')
    print(response)
    
    # Test OCR
    print("\nTesting OCR:")
    response = agent.chat('Extract text from "document.png"')
    print(response)
    
    # Test object detection
    print("\nTesting object detection:")
    response = agent.chat('Find cars in "street.jpg"')
    print(response)
    
    # Test visualization
    print("\nTesting visualization:")
    response = agent.chat("Visualize the results")
    print(response) 