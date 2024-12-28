from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from mira_sdk import MiraClient
from PyPDF2 import PdfReader
import io
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize MiraClient with your API key
client = MiraClient(config={"API_KEY": "sb-ed1b1b2d8e10ceda7513b1dfbc8ab880"})

# Flow configuration
FLOW_AUTHOR = "akasxh"
FLOW_NAME = "jobmatchai-resume-optimizer"
FLOW_VERSION = "2.0.0"

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    Args:
        pdf_file: File object containing PDF data
    Returns:
        str: Extracted text content
    Raises:
        Exception: If PDF processing fails
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text_content = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        return ' '.join(text_content).strip()
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        raise Exception(f"Failed to process PDF: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/generate-text", methods=["POST"])
def generate_text():
    try:
        # Get PDF file and job description
        pdf_file = request.files.get("pdf")
        job_description = request.form.get("job_description")

        # Validate inputs
        if not pdf_file:
            return jsonify({"error": "PDF file is required"}), 400
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400
        
        # Validate PDF file type
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Uploaded file must be a PDF"}), 400

        # Read PDF content
        pdf_content = pdf_file.read()
        
        # Extract text from PDF
        resume_content = extract_text_from_pdf(io.BytesIO(pdf_content))
        
        if not resume_content:
            return jsonify({"error": "Could not extract text from PDF. Please ensure the PDF contains readable text."}), 400

        # Prepare input data for the flow
        input_data = {
            "resume": resume_content,
            "job_description": job_description.strip()
        }

        # Construct flow name and execute
        flow_name = f"{FLOW_AUTHOR}/{FLOW_NAME}/{FLOW_VERSION}"
        logger.info(f"Executing flow: {flow_name}")
        result = client.flow.execute(flow_name, input_data)
        
        # Format response to match frontend expectations
        return jsonify({
            "success": True,
            "generated_text": result.get("text", "No text generated"),  # Adjust this based on your Mira flow's actual response structure
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Ensure static folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)