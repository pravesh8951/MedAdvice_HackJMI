from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

def process_text(extracted_text):
    try:
        # Use Google Gemini API for medical advice
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Based on this suggest me some advice what precautions to take {extracted_text}"
        )

        # Extract text response
        advice = response.text.strip() if response else "Failed to get advice from  API."

    except Exception as e:
        advice = f"Error: {str(e)}"

    return advice
