from flask import Flask, render_template, request, jsonify
from mira_sdk import MiraClient

app = Flask(__name__)

# Initialize MiraClient with your API key
client = MiraClient(config={"API_KEY": "sb-ed1b1b2d8e10ceda7513b1dfbc8ab880"})

# Flow name and version
FLOW_AUTHOR = "akasxh"
FLOW_NAME = "jobmatchai-resume-optimizer"
FLOW_VERSION = "1.0.0"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get inputs from the form
        job_description = request.form.get("jobDescription")
        resume = request.form.get("resume")

        if not job_description or not resume:
            return jsonify({"error": "Both resume and job description are required!"})

        # Prepare input data for the flow
        input_data = {
            "resume": resume,
            "job_description": job_description
        }

        # Construct the flow name
        flow_name = f"{FLOW_AUTHOR}/{FLOW_NAME}/{FLOW_VERSION}"

        try:
            # Execute the flow
            result = client.flow.execute(flow_name, input_data)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": f"Flow execution failed: {str(e)}"})
        
        print(f"Template folder: {app.template_folder}")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
