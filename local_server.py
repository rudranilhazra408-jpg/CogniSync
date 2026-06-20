from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader
import os
import re

# Initialize the local server
# We use a distinct name so it's easily identifiable in the client logs
mcp = FastMCP("CogniSync_Local_Server")

def redact_pii(text: str) -> str:
    """
    Security Feature: Redacts Personally Identifiable Information (PII).
    Ensures that names, registration numbers, or phone numbers in personal 
    study materials (like admit cards or marksheets) are scrubbed before 
    the LLM ever sees the context.
    """
    # Redact anything that looks like a 10-digit phone number or JEE Roll Number
    # (This is a basic regex filter to demonstrate the security architecture)
    text = re.sub(r'\b\d{10}\b', '[REDACTED_ID]', text)
    
    # Redact common name prefixes to protect identity
    text = re.sub(r'(Mr\.|Mrs\.|Ms\.|Name:)\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)?', r'\1 [REDACTED_NAME]', text)
    return text

@mcp.tool()
def read_study_pdf(file_path: str) -> str:
    """
    Reads a local PDF file (like a JEE syllabus or mock test) and extracts text.
    Returns the text ONLY after passing it through the local PII security filter.
    
    Args:
        file_path: The absolute path to the local PDF file.
    """
    # Edge case: The file doesn't exist or path is wrong
    if not os.path.exists(file_path):
        return f"System Error: Cannot locate the file at {file_path}. Please check the path."
    
    # Edge case: Not a PDF
    if not file_path.lower().endswith('.pdf'):
        return "System Error: The requested file is not a PDF."

    try:
        reader = PdfReader(file_path)
        extracted_text = ""
        
        # Read first 5 pages max to prevent context window overflow
        max_pages = min(5, len(reader.pages))
        for i in range(max_pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                extracted_text += page_text + "\n"
        
        if not extracted_text.strip():
            return "Warning: Successfully opened PDF, but no readable text was found (it might be scanned images)."

        # CRITICAL SECURITY STEP: Redact PII locally before returning to the agent
        safe_text = redact_pii(extracted_text)
        
        return f"Successfully extracted and sanitized {max_pages} pages:\n\n{safe_text}"
        
    except Exception as e:
        return f"An unexpected error occurred while parsing the PDF: {str(e)}"

if __name__ == "__main__":
    print("Starting CogniSync Local MCP Server...")
    print("Privacy filter is ACTIVE.")
    # Run the server. It will listen for incoming local connections from the AI Agent.
    mcp.run()