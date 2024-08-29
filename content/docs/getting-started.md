+++
title = 'Getting started'
date = 2024-08-14T08:22:26+02:00
draft = false
weight = 1
+++

### 1. Install Docker

Follow the official installation instructions to [install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

### 2. Start the installation

#### Download helper script

We have created a helper script to get you started with all necessary configuration.
Download the script here:

```shell
curl -s -O https://raw.githubusercontent.com/openrelik/openrelik-deploy/main/docker/deploy_openrelik.sh
```

#### Choose location for the installation
You can choose to host the OpenRelik data directory anywhere but note that by default it will host Artifacts and PostgreSQL data in this directory so make sure you have enough disk space available.

```shell
cd /opt
```

#### Run deployment script
```shell
sudo bash ~/deploy_openrelik.sh
```

#### Edit config.env and change OPENRELIK_SERVER_URL, if you are not running on localhost.
```shell
OPENRELIK_SERVER_URL=http(s)://your.server.url
```

#### Create OAuth credentials in a Google Cloud project
https://developers.google.com/workspace/guides/create-credentials#oauth-client-id

#### Edit config/settings.toml
```shell
client_id = "<CLIENT ID FROM PREVIOUS STEP>"
client_secret = "<CLIENT SECRET FROM PREVIOUS STEP>"
```

### 3. Start the system
```shell
cd openrelik
sudo docker compose up -d
```
