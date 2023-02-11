# Hasty Challange

This web application is built on Django framework. Users are able to use API key and URL to establish connection with the workspace. On the main page, users are able to choose JSON file, choose multiple images, create new project or choose existing projects, also according to chosen project, be able to see the available datasets or create new dataset, and based on the attributes of JSON file, be able to choose which annotations that will be uploaded to the project.

## Features to be added
- Ability to delete projects
- Show more detailed information on projects: number of pictures/annotations
- A dynamic console, where the progress will be shown when uploading the data
- Dynamic annotations checkboxes, based on the JSON file provided

## To fix
- Only when the project buttons are clicked, dataset buttons appear dynamically. Checking for the value inside the input field and getting datasets is a better way to go. For now when the input field is cleared, dataset buttons will not disappear
- More exception handling, a lot more.