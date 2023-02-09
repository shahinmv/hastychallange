from hasty import Client
import json
import glob
import os
from tqdm import tqdm

API_KEY = "iv8DaE00dXbFY568-FCVmMH320KWX8UNWunQMA9YKH8cFCMay-heLM8sBOI_EJIta5GKnTud-nQyg4gnz9ZaFw"
BASE_URL = "https://api-default-none-staging.dev.hasty.ai"

def progress_bar(current, total):
    percent = 100 * (current / total)
    bar = '█' * int(percent / 4) + '-' * (25 - int(percent / 4))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

def read_json():
    with open("Cable Cars Labels.json", "r") as file:
        return json.load(file)

def establish_connection():
    try:
        client = Client(api_key=API_KEY, base_url=BASE_URL)
        workspaces = client.get_workspaces()
        print("Connection established successfully!")
    except:
        raise Exception("Connection failed! Check API Key and URL.")
    else:
        return client, workspaces[0]

def create_project(client, workspace, name="Challenge", description="This is the Hasty Challenge"):
    return client.create_project(workspace=workspace, name=name, description=description)

def upload_images(project, folders):
    image_files = []
    for folder in folders:
        print(f"Uploading images from '{folder}' folder:")
        for i, file in enumerate(glob.glob(f"{folder}/*.jpg"), start=1):
            image_files.append(project.upload_from_file(dataset=project.create_dataset(folder), filepath=file))
            progress_bar(i, len(glob.glob(f"{folder}/*.jpg")))
        print()
    return image_files

if __name__ == "__main__":
    client, workspace = establish_connection()
    project = create_project(client, workspace)
    images = upload_images(project, ["Default", "new-data"])
    print("\nDone")