+++
title = 'API'
linkTitle = 'API docs'
date = 2026-02-12
draft = false
weight = 6
+++

This documentation provides an overview to the RESTful API endpoints that power the digital forensics platform. This API allows you to interact with the platform programmatically, enabling automation and integration with your existing tools and workflows. Full API documentation is provided when installing the server.

{{< callout type="info" >}}
If you want to access the API server and the generated documentation:

```shell
http://localhost:8710/api/v1/docs/
```

{{< /callout >}}

### Key Concepts

- **Authentication:** API requests require authentication using API keys associated with your user account. You can manage your API keys via the `/users/me/apikeys/` endpoints.
- **Resources:** The API is organized around resources such as `Users`, `Configs`, `Files`, `Folders`, and `Workflows`. Each resource has associated endpoints for performing actions on those resources.
- **HTTP Methods:** The API uses standard HTTP methods (GET, POST, PATCH, DELETE) to perform CRUD (Create, Read, Update, Delete) operations on resources.
- **Responses:** API responses are typically in JSON format, providing structured data about the requested resources or operations.
