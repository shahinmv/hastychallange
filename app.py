from hasty import Client
import json
import glob
import os
from tqdm import tqdm

API_KEY = "iv8DaE00dXbFY568-FCVmMH320KWX8UNWunQMA9YKH8cFCMay-heLM8sBOI_EJIta5GKnTud-nQyg4gnz9ZaFw"
BASE_URL = "https://api-default-none-staging.dev.hasty.ai"

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

def read_json():
    with open("Cable Cars Labels.json", "r") as file:
        return json.load(file)

def establish_connection(api, url):
    return Client(api_key=api, base_url=url)

def set_project():
    try:
        workspaces = h.get_workspaces()
    except:
        raise Exception("Connection failed! Check for API Key or the URL.")
    else:
        print("Connection successful!")
        default_workspace = workspaces[0]
        return h.create_project(workspace = default_workspace,
                                name = "Challange",
                                description = "This is the Hasty challange")

def set_labels(data):
    list_labels = []
    for x in data['label_classes']:
        list_labels.append(new_project.create_label_class(name=x['class_name'], class_type=x['class_type'], color=x['color'], 
                                                        norder=x['norder'])) 
    
    print("Label classes are set!")
    return list_labels

def upload_images():
    list_images = []

    print("Uploading images from 'Default' folder:")
    progress_bar(0, len(glob.glob(f"Default/*.jpg")))
    for counter, file in enumerate(glob.glob(f"Default/*.jpg"), start=0):
        list_images.append(new_project.upload_from_file(dataset=default_data,
                                            filepath=f"Default/{os.path.basename(file)}"))
        progress_bar(counter + 1, len(glob.glob(f"Default/*.jpg"))) 

    print("\nUploading images from 'new-data' folder:")
    progress_bar(0, len(glob.glob(f"new-data/*.jpg")))
    for counter, file in enumerate(glob.glob(f"new-data/*.jpg"), start=0):
        list_images.append(new_project.upload_from_file(dataset=new_data,
                                            filepath=f"new-data/{os.path.basename(file)}"))
        progress_bar(counter + 1, len(glob.glob(f"new-data/*.jpg")))

def set_attributes():
    list_attributes = []
    for x in data['attributes']:
        list_attributes.append(new_project.create_attribute(name=x['name'], attribute_type=x['type'], values=x['values'], norder=0))
    
    return list_attributes

if __name__=="__main__":
    h = establish_connection(API_KEY, BASE_URL)
    new_project = set_project()
    data = read_json()
    classes = set_labels(data)

    default_data = new_project.create_dataset("Default")
    new_data = new_project.create_dataset("new-data")
    images = upload_images() 

    attributes = set_attributes()
    print("\nDone")
    