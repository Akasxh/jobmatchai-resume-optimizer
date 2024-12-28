from flask import Flask, render_template, request, jsonify, url_for
from mira_sdk import MiraClient
from PyPDF2 import PdfReader
import io
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MiraClient with your API key
client = MiraClient(config={"API_KEY": "sb-ed1b1b2d8e10ceda7513b1dfbc8ab880"})

# Flow configuration
FLOW_AUTHOR = "akasxh"
FLOW_NAME = "jobmatchai-resume-optimizer"
FLOW_VERSION = "2.0.0"

def extract_text_from_pdf(pdf_file):
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

@app.route("/generate-text", methods=["POST"])
def generate_text():
    try:
        pdf_file = request.files.get("pdf")
        job_description = request.form.get("job_description")

        if not pdf_file:
            return jsonify({"error": "PDF file is required"}), 400
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400

        resume_content = extract_text_from_pdf(pdf_file)
        
        if not resume_content:
            return jsonify({"error": "Could not extract text from PDF. Please ensure the PDF contains readable text."}), 400

        input_data = {
            "resume": resume_content,
            "job_description": job_description.strip()
        }

        flow_name = f"{FLOW_AUTHOR}/{FLOW_NAME}/{FLOW_VERSION}"
        logger.info(f"Executing flow: {flow_name}")
        
        result = client.flow.execute(flow_name, input_data)
        
        # Log the result structure to understand what we're getting
        logger.info(f"Mira Flow Result: {result}")
        
        # Return the text content from the result
        # Assuming the LLM output is in the 'response' field
        generated_text = result.get('response', str(result))
        
        return jsonify({
            "success": True,
            "generated_text": generated_text
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.run(debug=True)