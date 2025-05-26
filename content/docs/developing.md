+++
title = 'Development'
date = 2025-05-26
draft = false
weight = 1
+++

{{< callout type="info" >}}
This development guide will help you install OpenRelik on your local machine.
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

When that is done we can start the OpenRelik stack with the plaso worker source to develop on. 

```bash
cd ../openrelik-worker-plaso
tilt up
```

This will build the openrelik-worker-plaso container from the cloned source and startup the complete stack using docker compose.

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

### Stop all stack down

You can bring down the complete stack with

```bash
tilt down
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

## Contributing to OpenRelik

We welcome contributions! Please see:

[https://github.com/google/.github/blob/master/CONTRIBUTING.md](Contributing)

### Finding Issues

* If you find any issues, please raise an issue with as much details as possible.

## Useful Resources

- **Project Website:** [Link to OpenRelik website](https://openrelik.org/)
- **How to create a new Worker:** [https://openrelik.org/guides/create-a-new-worker/](Create a new worker)