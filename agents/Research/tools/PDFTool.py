from agency_swarm.tools import BaseTool
from pydantic import Field
from playwright.sync_api import sync_playwright
import pypdf
import os
from io import BytesIO

class PDFTool(BaseTool):
    """
    A tool for PDF-related operations including generating PDFs from web pages
    and extracting text from existing PDFs.
    """
    
    url_or_file: str = Field(
        ..., 
        description="URL of the webpage to convert to PDF or path to the PDF file to process"
    )
    
    operation: str = Field(
        ..., 
        description="Operation to perform: 'generate' for creating PDF from webpage, 'extract' for extracting text from PDF"
    )
    
    output_path: str = Field(
        None, 
        description="Optional path where to save the generated PDF"
    )

    def run(self):
        """
        Execute the PDF operation based on the specified parameters.
        """
        try:
            if self.operation.lower() == 'generate':
                # Generate PDF from webpage using Playwright
                if not self.output_path:
                    self.output_path = 'output.pdf'
                
                with sync_playwright() as p:
                    # Launch browser
                    browser = p.chromium.launch()
                    page = browser.new_page()
                    
                    # Navigate to URL
                    page.goto(self.url_or_file)
                    # Wait for network to be idle
                    page.wait_for_load_state("networkidle")
                    
                    # Generate PDF
                    page.pdf(path=self.output_path)
                    
                    browser.close()
                    
                return f"PDF generated successfully and saved to {self.output_path}"
                
            elif self.operation.lower() == 'extract':
                # Extract text from PDF
                if not os.path.exists(self.url_or_file):
                    return f"Error: PDF file not found at {self.url_or_file}"
                
                with open(self.url_or_file, 'rb') as file:
                    # Create PDF reader object
                    pdf_reader = pypdf.PdfReader(file)
                    
                    # Extract text from all pages
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    
                    return text
                    
            else:
                return f"Error: Invalid operation '{self.operation}'. Use 'generate' or 'extract'."
                
        except Exception as e:
            return f"Error processing PDF: {str(e)}"

if __name__ == "__main__":
    # Test PDF generation
    tool = PDFTool(
        url_or_file="https://www.example.com",
        operation="generate",
        output_path="test.pdf"
    )
    print(tool.run())
    
    # Test PDF text extraction
    tool = PDFTool(
        url_or_file="test.pdf",
        operation="extract"
    )
    print(tool.run()) 