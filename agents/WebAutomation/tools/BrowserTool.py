from agency_swarm.tools import BaseTool
from pydantic import Field
from playwright.sync_api import sync_playwright
import os
import json

class BrowserTool(BaseTool):
    """
    A tool for web automation tasks including navigation, form filling, data extraction,
    and interaction with web elements using Playwright.
    """
    
    action: str = Field(
        ..., 
        description="Action to perform: 'navigate', 'fill_form', 'extract_data', 'screenshot'"
    )
    
    url: str = Field(
        None, 
        description="URL to navigate to"
    )
    
    form_data: dict = Field(
        None, 
        description="Dictionary containing form field names and values"
    )
    
    selector: str = Field(
        None, 
        description="CSS selector for element interaction or data extraction"
    )
    
    data_type: str = Field(
        None, 
        description="Type of data to extract: 'text', 'links', 'images', etc."
    )
    
    output_path: str = Field(
        None, 
        description="Path where to save screenshots or other output files"
    )

    def run(self):
        """
        Execute the web automation action based on the specified parameters.
        """
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch()
                page = browser.new_page()
                
                if self.action == 'navigate':
                    if not self.url:
                        return "Error: URL required for navigation"
                    
                    # Navigate to URL
                    page.goto(self.url)
                    # Wait for network to be idle
                    page.wait_for_load_state("networkidle")
                    return f"Successfully navigated to {self.url}"
                
                elif self.action == 'fill_form':
                    if not self.form_data:
                        return "Error: Form data required for form filling"
                    
                    # Fill form fields
                    filled_fields = []
                    for field_name, value in self.form_data.items():
                        try:
                            # Try different selectors for form fields
                            selectors = [
                                f"input[name='{field_name}']",
                                f"textarea[name='{field_name}']",
                                f"select[name='{field_name}']",
                                f"#{field_name}",  # ID selector
                                f"[data-field='{field_name}']",  # Data attribute selector
                                f"[aria-label='{field_name}']",  # ARIA label selector
                                f"[placeholder*='{field_name}' i]",  # Placeholder contains field name (case-insensitive)
                                f"input[type='text']",  # Any text input
                                f"input[type='search']",  # Any search input
                                f"input:not([type])",  # Input without type
                                f"textarea",  # Any textarea
                                f"[contenteditable='true']"  # Contenteditable elements
                            ]
                            
                            field_found = False
                            for selector in selectors:
                                try:
                                    # Wait for element with a shorter timeout
                                    field = page.wait_for_selector(selector, timeout=5000)
                                    if field and field.is_visible():
                                        field.fill(str(value))
                                        filled_fields.append(field_name)
                                        field_found = True
                                        break
                                except:
                                    continue
                            
                            if not field_found:
                                # Try to find any visible input field
                                inputs = page.query_selector_all("input:visible")
                                for input_field in inputs:
                                    try:
                                        if input_field.is_visible():
                                            input_field.fill(str(value))
                                            filled_fields.append(field_name)
                                            field_found = True
                                            break
                                    except:
                                        continue
                            
                            if not field_found:
                                return f"Error: Could not find form field '{field_name}'"
                                
                        except Exception as e:
                            return f"Error filling field '{field_name}': {str(e)}"
                    
                    # Try to find and click submit button
                    submit_selectors = [
                        "input[type='submit']",
                        "button[type='submit']",
                        "button:has-text('Submit')",
                        "button:has-text('Search')",
                        "button:has-text('Send')",
                        "button:has-text('Go')",
                        "[role='button']",
                        "button",
                        "input[type='button']"
                    ]
                    
                    for selector in submit_selectors:
                        try:
                            submit = page.wait_for_selector(selector, timeout=5000)
                            if submit and submit.is_visible():
                                submit.click()
                                page.wait_for_load_state("networkidle")
                                break
                        except:
                            continue
                    
                    return f"Successfully filled form fields: {', '.join(filled_fields)}"
                
                elif self.action == 'extract_data':
                    if not self.selector or not self.data_type:
                        return "Error: Selector and data type required for data extraction"
                    
                    # Wait for elements to be available
                    page.wait_for_load_state("networkidle")
                    
                    # Extract data based on type
                    if self.data_type == 'text':
                        elements = page.query_selector_all(self.selector)
                        texts = [elem.inner_text() for elem in elements if elem.is_visible()]
                        return json.dumps(texts)
                        
                    elif self.data_type == 'links':
                        elements = page.query_selector_all(self.selector)
                        links = [elem.get_attribute('href') for elem in elements if elem.is_visible()]
                        return json.dumps(links)
                        
                    else:
                        return f"Error: Unsupported data type '{self.data_type}'"
                
                elif self.action == 'screenshot':
                    if not self.output_path:
                        self.output_path = 'screenshot.png'
                    
                    # Wait for page to be ready
                    page.wait_for_load_state("networkidle")
                    
                    # Take screenshot
                    page.screenshot(path=self.output_path)
                    return f"Screenshot saved to {self.output_path}"
                
                else:
                    return f"Error: Invalid action '{self.action}'"
                
                browser.close()
                
        except Exception as e:
            return f"Error during web automation: {str(e)}"

if __name__ == "__main__":
    # Test navigation
    tool = BrowserTool(
        action="navigate",
        url="https://www.example.com"
    )
    print("Testing navigation:", tool.run())
    
    # Test form filling
    tool = BrowserTool(
        action="fill_form",
        form_data={
            "search": "test",
            "category": "docs"
        }
    )
    print("Testing form filling:", tool.run())
    
    # Test data extraction
    tool = BrowserTool(
        action="extract_data",
        selector="h1",
        data_type="text"
    )
    print("Testing data extraction:", tool.run())
    
    # Test screenshot
    tool = BrowserTool(
        action="screenshot",
        output_path="test_screenshot.png"
    )
    print("Testing screenshot:", tool.run()) 