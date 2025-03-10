import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import json
import yaml
import base64
from create_visualization import create_visualization, create_dashboard
from ai import ask_ai_to_create_dashboard_visualizations, ask_ai_to_create_dashboard

load_dotenv()  # take environment variables from .env.


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "examples/dashboard.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)

vizs = ask_ai_to_create_dashboard_visualizations(base64_image)
for viz in vizs:
    create_visualization(str(viz), False)
dashboard = ask_ai_to_create_dashboard(base64_image)
create_dashboard(dashboard)