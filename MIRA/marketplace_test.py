from mira_sdk import MiraClient, Flow
import os

# Load environment variables from .env file
#load_dotenv()

#api_key = os.getenv("API_KEY")

api_key = 'sb-ed1b1b2d8e10ceda7513b1dfbc8ab880'

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

input_data = {"topic": "AI for detection", "style": "Deep Learning", "time_constraint": "12hrs"}

# If no version is provided it'll use latest version by default
if version:
	flow_name = f"Akasxh/Hackathon-Idea-generation/{version}"
else:
	flow_name = "Akasxh/Hackathon-Idea-generation"

result = client.flow.execute(flow_name, input_data)
print(result)