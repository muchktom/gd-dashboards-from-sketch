from openai import OpenAI
from pathlib import Path
import json
import os


def load_directory_into_string(directory_path):
    # Convert directory_path to a Path object
    directory = Path(directory_path)
    
    # Initialize an empty string to hold the contents
    all_contents = ""

    # Iterate through each file in the directory
    for file_path in directory.iterdir():
        if file_path.is_file():  # Make sure it's a file
            all_contents += file_path.read_text() + "\n"

    # Return the combined contents of all files
    return all_contents

def ask_ai_to_create_dashboard_visualizations(base64_image):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    INSTRUCTIONS = Path('prompts/visualization_builder.txt').read_text()
    PROMPT_DATASETS = load_directory_into_string('analytics/datasets')
    PROMPT_EXAMPLES_OF_VISUALIZATION = load_directory_into_string('analytics/visualisations')
    PROMPT_METRICS = load_directory_into_string('analytics/metrics')
    schema = json.loads(Path('prompts/visualizations_schema.json').read_text())

    outcome = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "assistant", "content": "Here are the fields from which you can build visualizations. Use only existing attributes and facts."+ PROMPT_DATASETS},
            {"role": "assistant", "content": "Here are examples of existing visualizations: " + PROMPT_EXAMPLES_OF_VISUALIZATION},
            {"role": "assistant", "content": "Here are the metrics from which you can build visualizations. Use only existing metrics." + PROMPT_METRICS},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Identify visualisations (charts) on the image and map it to the described visualization structure. Use the available fields. If not found, use the most similar fields. Prefix visualisation id with 'napkin_'. Do not take the filters into account, unless these are metric filters or ranking filters.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ], 
        response_format = schema
    )

    return json.loads(outcome.choices[0].message.content).get('visualisations')

def ask_ai_to_create_dashboard(base64_image):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    INSTRUCTIONS = Path('prompts/dashboard_builder.txt').read_text()
    PROMPT_DATASETS = load_directory_into_string('analytics/datasets')
    PROMPT_EXAMPLES_OF_VISUALIZATION = load_directory_into_string('analytics/visualisations')
    PROMPT_EXAMPLES_OF_DASHBOARDS = load_directory_into_string('analytics/dashboards')
    schema = json.loads(Path('prompts/dashboard_schema.json').read_text())

    outcome = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "assistant", "content": "Here are the fields from which you can build dashboard filters."+ PROMPT_DATASETS},
            {"role": "assistant", "content": "Here are existing visualizations which you can use when building dashboard: " + PROMPT_EXAMPLES_OF_VISUALIZATION},
            {"role": "assistant", "content": "Here are already existing dashboards to learn from: " + PROMPT_EXAMPLES_OF_DASHBOARDS},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Map what is on the image to the described dashboard structure. Use existing visualizations and connect it to the newly created dashboard.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ], 
        response_format = schema
    )
    return outcome.choices[0].message.content