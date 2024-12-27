from mira_sdk import MiraClient, Flow
import os

# Load environment variables from .env file
#load_dotenv()

#api_key = os.getenv("API_KEY")

api_key = 'sb-ed1b1b2d8e10ceda7513b1dfbc8ab880'

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

flow = Flow(source="flow.yaml")

input_dict = {"resume": "BTech in AI from IITP, excell in deep learning", "job_description": "SWE Intern at Amazon"}

response = client.flow.test(flow, input_dict)

print(response)