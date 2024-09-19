+++
title = 'API'
linkTitle = 'API docs'
date = 2024-08-14T08:22:26+02:00
draft = false
weight = 5
+++

This documentation provides an overview to the RESTful API endpoints that power the digital forensics platform. This API allows you to interact with the platform programmatically, enabling automation and integration with your existing tools and workflows. Full API documentation is provided when installing the server.

{{< callout type="info" >}}
The complete (auto-generated) documentation can be found at http://<OPENRELIK_SERVER_HOSTNAME>/docs
{{< /callout >}}

### Key Concepts

* **Authentication:** API requests require authentication using API keys associated with your user account. You can manage your API keys via the `/users/me/apikeys/` endpoints.
* **Resources:** The API is organized around resources such as `Users`, `Configs`, `Files`, `Folders`, and `Workflows`. Each resource has associated endpoints for performing actions on those resources.
* **HTTP Methods:** The API uses standard HTTP methods (GET, POST, PATCH, DELETE) to perform CRUD (Create, Read, Update, Delete) operations on resources.
* **Responses:** API responses are typically in JSON format, providing structured data about the requested resources or operations.

### API Endpoints

#### Users

* **GET /users/me/**: Get information about the currently authenticated user.
* **GET /users/me/apikeys/**: Retrieve the API keys associated with the current user.
* **POST /users/me/apikeys/**: Create a new API key for the current user.

#### Configs

* **GET /configs/system/**: Retrieve the system configuration settings.

#### Files

* **GET /files/{file_id}**: Get details about a specific file.
* **DELETE /files/{file_id}**: Delete a file.
* **GET /files/{file_id}/content**: Retrieve the content of a file.
* **POST /files/{file_id}/download**: Initiate the download of a file.
* **GET /files/{file_id}/download_stream**: Stream the content of a file for download.
* **POST /files/**: Create a new file.
* **GET /files/{file_id}/workflows**: Retrieve all workflows associated with a file.
* **GET /files/{file_id}/workflows/{workflow_id}/tasks/{task_id}**: Get details about a specific task within a workflow associated with a file.
* **POST /files/{file_id}/workflows/{workflow_id}/tasks/{task_id}/download**: Download the result of a task.
* **GET /files/{file_id}/summaries/{summary_id}**: Retrieve a specific file summary.
* **POST /files/{file_id}/summaries**: Generate a summary for a file.

#### Folders

* **GET /folders/**: Retrieve the root folders.
* **POST /folders/**: Create a new folder.
* **GET /folders/{folder_id}**: Get details about a specific folder.
* **PATCH /folders/{folder_id}**: Update a folder's information.
* **DELETE /folders/{folder_id}**: Delete a folder.
* **GET /folders/{folder_id}/folders/**: Retrieve subfolders within a folder.
* **GET /folders/{folder_id}/files/**: Retrieve files within a folder.
* **GET /folders/{folder_id}/workflows**: Retrieve workflows associated with a folder.

#### Workflows

* **GET /workflows/{workflow_id}**: Retrieve details about a workflow.
* **PATCH /workflows/{workflow_id}**: Update a workflow's information.
* **DELETE /workflows/{workflow_id}**: Delete a workflow.
* **POST /workflows/**: Create a new workflow.
* **POST /workflows/{workflow_id}/copy/**: Create a copy of a workflow.
* **POST /workflows/run/**: Run a workflow.
* **GET /workflows/templates**: Retrieve workflow templates.
* **POST /workflows/templates/**: Create a new workflow template.
* **GET /workflows/registered_tasks/**: Retrieve the list of registered tasks.


**Note:** This overview provides a high-level summary of the API endpoints. For detailed information on request parameters, response formats, and error handling, please refer to the full API documentation provided when installing the server.
