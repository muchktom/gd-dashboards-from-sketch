import yaml
import os
from pathlib import Path

def create_visualization(visualization, deploy=True):
    visualization = yaml.safe_load(visualization)
    title = "napkin_" + visualization.get("title").replace(" ", "_") + ".yaml"

    # Define the output directory and file path
    output_directory = Path("analytics/visualisations")
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file_path = output_directory / title
    print(output_file_path)

    # Save the content to the file, replacing it if it exists
    with open(output_file_path, "w") as output_file:
        yaml.dump(visualization, output_file, default_flow_style=False)
    if deploy:
        deploy_analytics()
    return visualization.get("id")

def deploy_analytics():
    result = os.system("gd deploy")
    if result != 0:
        raise RuntimeError("gd deploy failed")

def create_dashboard(dashboard, deploy=True):
    dashboard = yaml.safe_load(dashboard)
    title = "napkin_" + dashboard.get("title").replace(" ", "_") + ".yaml"

    # Define the output directory and file path
    output_directory = Path("analytics/dashboards")
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file_path = output_directory / title
    print(output_file_path)

    # Save the content to the file, replacing it if it exists
    with open(output_file_path, "w") as output_file:
        yaml.dump(dashboard, output_file, default_flow_style=False)
    if deploy:
        deploy_analytics()
    return dashboard.get("id")

