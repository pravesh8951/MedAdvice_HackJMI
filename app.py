from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv
from chatbot import process_text

# Load environment variables
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set Tesseract path (Change this if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # 🛑 **Fix: Perform OCR Extraction**
            image = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(image)

            print("Extracted Text:", extracted_text)  # Debugging step

            # Send extracted text to chatbot
            response = process_text(extracted_text)

            return jsonify({"text": extracted_text, "response": response})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
