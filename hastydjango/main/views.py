from django.shortcuts import render, redirect
from hasty import Client
from django.contrib import messages
import json
import uuid
from django.core.cache import cache

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
    if request.method == "POST":
        client = cache.get('client')
        print(type(client))
        json_file = request.FILES.get('json_file')
        images = request.FILES.getlist('images')
        workspace = request.POST.get('workspace')
        project = request.POST.get('project')
        description = request.POST.get('description')


        new_project = set_project(client, workspace, project, description)
        train_dataset = new_project.create_dataset("train")
        for image in images:
            new_project.upload_from_url(dataset=train_dataset,
                                    filename='4.jpg',
                                    url={'image': image})
        
    return render(request, 'main/index.html')