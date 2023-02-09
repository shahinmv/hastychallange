from hasty import Client
import json
import glob
import os

API_KEY = "iv8DaE00dXbFY568-FCVmMH320KWX8UNWunQMA9YKH8cFCMay-heLM8sBOI_EJIta5GKnTud-nQyg4gnz9ZaFw"
BASE_URL = "https://api-default-none-staging.dev.hasty.ai"

def progress_bar(current, total):
    percent = 100 * (current / total)
    bar = '█' * int(percent / 4) + '-' * (25 - int(percent / 4))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

def read_json(file_path: str) -> dict:
    """Read the JSON file and return its content as a dictionary."""
    with open(file_path, "r") as file:
        return json.load(file)

def establish_connection(api_key: str, base_url: str) -> Client:
    """Create a connection to the Hasty API using the provided API key and base URL."""
    try:
        client = Client(api_key=api_key, base_url=base_url)
        client.get_workspaces()
        print("Connection successful!")
        return client
    except:
        raise Exception("Connection failed! Check for API Key or the URL.")

def set_project(client: Client, workspace_name: str, project_name: str, project_description: str) -> dict:
    """Create a new project in the specified workspace."""
    workspaces = client.get_workspaces()
    for workspace in workspaces:
        if workspace.name == workspace_name:
            return client.create_project(
                workspace=workspace,
                name=project_name,
                description=project_description
            )
    raise Exception(f"No workspace found with the name '{workspace_name}'")

def set_labels(project: dict, label_data: dict) -> list:
    """Create label classes in the project from the label data."""
    label_classes = []
    for label in label_data['label_classes']:
        label_classes.append(project.create_label_class(
            name=label['class_name'],
            class_type=label['class_type'],
            color=label['color'],
            norder=label['norder']
        ))
    print("Label classes are set!")
    return label_classes

def set_dataset(project: dict, names: list) -> list:
    datasets = []
    for name in names:
        datasets.append(project.create_dataset(name))
    return datasets

def upload_images(project: dict, folders: list, datasets: list) -> list:
    image_files = []
    for folder, dataset in zip(folders, datasets):
        print(f"Uploading images from '{folder}' folder:")
        for i, file in enumerate(glob.glob(f"{folder}/*.jpg"), start=1):
            image_files.append(project.upload_from_file(dataset=dataset, filepath=f"{folder}/{os.path.basename(file)}"))
            progress_bar(i, len(glob.glob(f"{folder}/*.jpg")))
        print()
    return image_files

def set_attributes(project: dict, attribute_data: dict) -> list:
    """Create attributes in the project from the attribute data."""
    attributes = []
    for attribute in attribute_data['attributes']:
        attributes.append(project.create_attribute(
            name=attribute['name'],
            attribute_type=attribute['type'],
            values=attribute['values'],
            norder=0
        ))
    return attributes

if __name__ == "__main__":
    h = establish_connection(API_KEY, BASE_URL)

    data = read_json("Cable Cars Labels.json")

    project = set_project(h, "Challange", "Challange", "This is the Hasty challenge")

    labels = set_labels(project, data)

    datasets = set_dataset(project, ['Default', 'new-data'])

    images = upload_images(project, ["Default", "new-data"], datasets)

    attributes = set_attributes(project, data)
