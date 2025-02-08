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

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/medical_advice")
def medical_advice():
    return render_template("medical_advice.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/inperson")
def inperson():
    return render_template("inperson.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Perform OCR Extraction
            image = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(image)

            print("Extracted Text:", extracted_text)  # Debugging step

            # Send extracted text to chatbot
            response = process_text(extracted_text)

            return jsonify({"text": extracted_text, "response": response})
    
    return jsonify({"error": "No file uploaded"}), 400

if __name__ == "__main__":
    app.run(debug=True)