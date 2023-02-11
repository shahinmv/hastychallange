from django.shortcuts import render, redirect
from hasty import Client
from django.contrib import messages
import json
import uuid
from django.core.cache import cache
from .models import Image
import os
from django.conf import settings
from django.http import JsonResponse


def get_domain(request):
    host = request.META['HTTP_HOST']
    return host


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


def set_labels(project: dict, label_data: dict):
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


def set_attributes(project: dict, attribute_data: dict):
    """Create attributes in the project from the attribute data."""
    attributes = []
    for attribute in attribute_data['attributes']:
        attributes.append(project.create_attribute(
            name=attribute['name'],
            attribute_type=attribute['type'],
            values=attribute['values'],
            norder=0
        ))
    print("Attributes are set!")


def upload_images(request, project, dataset):
    image_files = []
    print(f"Uploading images:")
    instances = Image.objects.all()
    for i, instance in enumerate(instances, start=1):
        print(instance.image.path)
        image_files.append(project.upload_from_file(
            dataset=dataset, filepath=instance.image.path))
       # progress_bar(i, len(glob.glob(f"{folder}/*.jpg")))
    print()


def login(request):
    if request.method == "POST":
        try:
            API_KEY = request.POST.get('api_key')
            BASE_URL = request.POST.get('url')

            client = Client(api_key=API_KEY, base_url=BASE_URL)
            client.get_workspaces()
        except:
            messages.info(request, "Connection failed! Check API key or URL")
        else:
            cache.set('client', client, timeout=None)
            return redirect('main')

    return render(request, 'authenticate/login.html')


def main(request):
    client = cache.get('client')
    workspaces = client.get_workspaces()
    projects = client.get_projects()

    deleteall()

    if request.method == "POST":
        json_file = request.FILES.get('json_file')
        try:
            data = json.loads(json_file.read().decode('utf-8'))
        except:
            print("JSON file not received")

        all_images = request.FILES.getlist('images')
        attributes_json = request.POST.getlist('parse_json')
        project = request.POST.get('project')
        description = request.POST.get('description')
        dataset = request.POST.get('dataset')

        for x in all_images:
            images = Image(image=x)
            images.save()

        current_project = next(
            (x for x in projects if project in x.name), None)

        if current_project is None:
            current_project = set_project(
                client, workspaces[0].name, project, description)

        if "label_classes" in attributes_json:
            set_labels(current_project, data)
        if "attributes" in attributes_json:
            set_attributes(current_project, data)

        datasets = current_project.get_datasets()
        current_dataset = next(
            (x for x in datasets if dataset in x.name), None)
        
        if current_dataset is None:
            current_dataset = current_project.create_dataset(dataset)

        upload_images(request, current_project, current_dataset)

        return redirect('main')

    return render(request, 'main/index.html', {'workspaces': workspaces, 'projects': projects})


def get_data(request):
    if request.method == "POST":
        client = cache.get('client')
        projects = client.get_projects()
        project = request.POST['projectName']

        current_project = next(
            (x for x in projects if project in x.name), None)
        datasets = current_project.get_datasets()

        data = {}
        for i, dataset in enumerate(datasets, start=0):
            data[i] = {"text": dataset.name}

        return JsonResponse(data, safe=False)


def deleteall():
    Image.objects.all().delete()
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            os.remove(os.path.join(root, file))

    print("Deleted all")
    return redirect(main)
