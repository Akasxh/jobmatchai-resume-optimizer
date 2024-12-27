from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
import os

# Load environment variables from .env file
#load_dotenv()

#api_key = os.getenv("API_KEY")

api_key = 'sb-ed1b1b2d8e10ceda7513b1dfbc8ab880'

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

# Test the flow locally
flow = Flow(source="flow.yaml")
try:
	client.flow.deploy(flow)    
except FlowError as e:
	print(f"Error occured: {str(e)}")