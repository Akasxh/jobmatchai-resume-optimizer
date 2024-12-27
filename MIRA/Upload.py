from mira_sdk import MiraClient, Flow
import os

# Load environment variables from .env file
#load_dotenv()

#api_key = os.getenv("API_KEY")

api_key = 'sb-ed1b1b2d8e10ceda7513b1dfbc8ab880'

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

# Create dataset
#client.dataset.create("akasxh/resume-dataset", "Employees with their resume and job")

# Add file to your dataset
client.dataset.add_source("akasxh/resume-dataset", file_path=r"C:\Users\draka\Downloads\UpdatedResumeDataSet.csv\UpdatedResumeDataSet.csv")