+++
title = 'Development'
date = 2025-05-26
draft = false
weight = 1
+++

{{< callout type="info" >}}
This development guide will help you install OpenRelik on your local machine for developing purposes.
{{< /callout >}}

# OpenRelik Development Guide

Welcome to the OpenRelik development guide! This document provides instructions and best practices for contributing to the OpenRelik project.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

- **Git:** For version control.
- **Python3**
- **Docker** See https://docs.docker.com/engine/install/ for several ways to install Docker.
- **[Tilt](https://docs.tilt.dev/)**

## Setting Up Your Development Environment

### Initial Environment Setup

This script will download the main deployment configuration and helper scripts.

```bash
mkdir -p openrelik-src && cd openrelik-src
wget -O install.sh https://raw.githubusercontent.com/openrelik/openrelik-deploy/main/docker/install.sh
```

### Installing Dependencies

This section focuses on installing Tilt, a key tool for the OpenRelik development workflow. Other project dependencies are typically managed within the Docker containers or by the `install.sh` script mentioned in other parts of this guide.

#### Installing Tilt

Tilt is a tool that automates deploying containers (often via Docker Compose), syncing file changes directly into running containers, and managing container restarts or rebuilds. This is highly beneficial for a smooth development experience, as it handles much of the repetitive build and deployment cycle for you. While Tilt is recommended, you can use Docker Compose's watch mode as an alternative for some scenarios if you prefer.

To install Tilt, you can download and run its official installation script:

```bash
wget -O install_tilt.sh https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh
bash install_tilt.sh
```

or use any other method listed on [docs.tilt.dev](https://docs.tilt.dev/)

## Building and Running OpenRelik for Development

This section guides you through the initial setup of the OpenRelik stack and then how to use Tilt to manage individual components for development.

### Initial Stack Setup with `install.sh`

First, run the `install.sh` script (downloaded in the "Initial Environment Setup" step) from your `openrelik-src` directory. This script initializes essential data directories, downloads default configurations, pulls the required Docker images for the core OpenRelik services, and then starts them using Docker Compose.

```bash
cd ..
pwd # should be ./openrelik-src
bash install.sh
```

This will pull the openrelik docker images, configure the data folders and start the stack. 

**Note:** Please review and copy the displayed username and password for initial login to the OpenRelik WebUI. It will not be shown again later.

### Disable docker

We do not want to run OpenRelik directly with docker compose as we will use Tilt to manage the development cycle we need to stop the stack after the initial configuration.

```bash
cd openrelik
docker compose down
```

### Startup OpenRelik

#### Tilt WebUI

Your Tilt WebUI is available as shown in the Tilt startup output (port 10350) where you can monitor container status and logs and force rebuilds.

#### OpenRelik WebUI

Your OpenRelik WebUI should be available on the URL (http://localhost:8711/ ) shown in the startup logs in Tilt.

#### OpenRelik API

OpenRelik API server listens on port 8710.

### Port forwarding

If you are deveolping on a remote sysystem, you might want to follow the following ports:

```bash
ssh -L 10350:localhost:10350 -L 8710:localhost:8710 -L 8711:localhost:8711 yourmachine.local
```

### Developing the Server with Hot Reloading

To speed up server-side development, you can configure the OpenRelik server (which typically uses `uvicorn`) to automatically reload when you make code changes. This avoids manual restarts and provides a faster feedback loop.

1.  **Locate your `docker-compose.yml` file:** This file is usually in the root of your `openrelik-deploy/docker/` directory or a similar location where your OpenRelik stack is defined.
2.  **Modify the server's command:** Find the service definition for the OpenRelik server (often named `openrelik-server` or `api`). You'll need to add the `--reload` and `--reload-dir` flags to the `uvicorn` command.

    For example, if the original command is:
    ```yaml
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    ```

    Change it to:
    ```yaml
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/openrelik/
    ```

    *   **`--reload`**: Tells `uvicorn` to watch for code changes and restart the server automatically.
    *   **`--reload-dir /app/openrelik/`**: Specifies the directory *inside the container* where your server's source code is mounted and should be monitored for changes. Adjust this path if your project structure is different.


3. **Create and adjust a Tiltfile** You need to change the TILTfile in `openrelik-src/oprenrelik-server/docker-compose.yml`: 

```version_settings(constraint=">=0.22.1")

docker_compose("../openrelik/docker-compose.yml")

docker_build(
    # Image name - must match the image in the docker-compose file
    "ghcr.io/openrelik/openrelik-server",
    # Docker context
    ".",
    live_update=[
        # Sync local files into the container.
        sync("./src", "/openrelik/src"),
        # Restart the process to pick up the changed files.
        restart_container(),
    ],
)
```

4.  **Restart your services:** After saving the `docker-compose.yml` file, restart your services (e.g., using `tilt up` if you're using Tilt).

```bash
cd openrelik-src/openrelik-server/
tilt up
```

Now, when you save changes to your Python files within the specified `--reload-dir`, `uvicorn` will automatically restart, applying your updates.

You will see in the tilt output something like:

```bash
...
openrelik-se… │ 1 File Changed: [src/admin.py]
openrelik-se… │ Will copy 1 file(s) to container: [openrelik-server]
openrelik-se… │ - '<FOLDER>/openrelik-src/openrelik-server/src/admin.py' --> '/app/openrelik/admin.py'
openrelik-se… │ RUNNING: tar -C / -x -f -
openrelik-se… │   → Container openrelik-server updated!
openrelik-se… │ INFO:     Will watch for changes in these directories: ['/app/openrelik']
...
```

### Create a new worker

Follow the guide [creating a new worker](../guides/create-a-new-worker.md).

### Stop all stack down

You can bring down the complete stack with

```bash
tilt down
```

## Administrative Tasks with admin.py

OpenRelik includes an admin.py script for performing various administrative tasks directly against the backend, such as creating users, listing users, or other management functions. 

This script is particularly useful for initial setup or when direct database manipulation is needed, for instance, if the initial admin credentials from install.sh were missed. 

### Accessing admin.py

The admin.py script is located within the openrelik-server container (or openrelik-api depending on your setup – typically the container running the FastAPI application). 

To use it, you first need to execute a shell session inside this running container: 
```bash 
# Ensure your OpenRelik stack is running (e.g., via 'tilt up' or 'docker compose up') 
# Replace 'openrelik-server' if your API container has a different name (e.g., openrelik-api) 
docker exec -it openrelik-server /bin/bash 
```

### Using admin.py

Once you are inside the container's shell, you can run the admin.py script.


```bash
python admin.py --help
# Inside the openrelik-server container python admin.py --help 
# To see available commands and options +python admin.py create-user --username newadmin --password yoursecurepassword --is-admin 
# Example + + +Refer to the script's help output (python admin.py --help or python admin.py <command> --help) for detailed usage instructions for each available command. 
```

## Running Unit Tests

At the moment, only some workers do have unit tests. To run them go into the worker and run:

```bash
python3 -m pytest tests/
```

## Debugging OpenRelik

With Tilt setup and the stack running it is easy to develop and debug. You can use VSCode to set breakpoints in the code and connect to the running worker using the provided launch profile (see `.vscode/launch.json`). Tilt will monitor the local files, sync any relevant file into the running container and restart the container. 

To enable Python debugging for a container, edit the `docker-compose.yml` file in the OpenRelik installation folder and add the below settings to your container configuration block

```yaml
...
environment:
- OPENRELIK_PYDEBUG=1
- OPENRELIK_PYDEBUG_PORT=5678
...
ports:
      - 5678:5678
...
```

## Coding Guidelines

### Code Style

* Please follow: https://google.github.io/styleguide/pyguide.html
* **Formatter:** Ruff is the official formatter. Configure your IDE to run Ruff on save.
* **String Quotes:** Use double quotes (") for strings unless single quotes (') avoid escaping.
* **Imports:**
    * Group imports into standard library, third-party, and OpenRelik modules.
    * Sort imports alphabetically within each group.
    * Use absolute imports whenever possible.
* **Type hints:**
    * We follow PEP 484. Type hinting is not yet fully implemented across the code base but we are working towards that goal.
* **Naming Conventions:**
    * Variables and functions: lower_case_with_underscores
    * Classes: CamelCase
    * Constants: UPPER_CASE_WITH_UNDERSCORES
* **Documentation:**
    * Use docstrings for all modules, classes, and functions.
    * Follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstring formatting.
        *API documentation is automatically generated by FastAPI from the code's docstrings, which is why it's helpful to follow a specific format.

## Contributing to OpenRelik

We welcome contributions! Please see:
 
[Contributing](https://github.com/google/.github/blob/master/CONTRIBUTING.md)

### Finding Issues

* If you find any issues, please raise an issues in the relevant repository (e.g. specific to a worker vs. server) with as much details as possible.
* More general feature discussions: [Github OpenRelik discussions](https://github.com/orgs/openrelik/discussions)

## Useful Resources

- **Project Website:** [Link to OpenRelik website](https://openrelik.org/)
- **How to create a new Worker:** [Create a new worker](https://openrelik.org/guides/create-a-new-worker/)

## FAQ

*   **Why am I redirected to the login page after entering valid credentials?**

    If you successfully log in but find yourself immediately redirected back to the login page, this often points to how your browser and the OpenRelik server are handling the session, specifically with regards to the hostname you're using (`localhost` vs. `127.0.0.1`).

    **Common Reasons & Solution:**

    *   **Cookie Domain/Origin Mismatch:** Web applications often set session cookies tied to a specific domain. If the cookie is set for `localhost`, your browser might not send it if you then access the application via `127.0.0.1` (or vice-versa), as they are technically treated as different origins. The server might also have security policies (like CORS or origin validation) that only recognize one of these hostnames.

    *   **Try the Alternative:** The simplest solution is to try accessing the OpenRelik WebUI using the other address.
        *   If you were using `http://127.0.0.1:8711`, try `http://localhost:8711`.
        *   If you were using `http://localhost:8711`, try `http://127.0.0.1:8711`.

    This usually resolves the issue by aligning the address you're using with how the server expects to manage your session.