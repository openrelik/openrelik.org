+++
title = 'Getting started'
date = 2024-09-10
draft = false
weight = 1
+++

{{< callout type="info" >}}
This installation guide will help you install OpenRelik on your local machine.
{{< /callout >}}

### 1. Install Docker

Follow the official installation instructions to [install Docker Engine](https://docs.docker.com/engine/install/) for your platform.

### 2. Start the installation

#### Download helper script

We have created a helper script to get you started with all necessary configuration.
Download the script here:

```shell
curl -s -O https://raw.githubusercontent.com/openrelik/openrelik-deploy/main/docker/install.sh
```

#### Choose location for the installation
You can choose to host the OpenRelik data directory anywhere but note that by default it will host Artifacts and PostgreSQL data in this directory so make sure you have enough disk space available.

```shell
cd <DIRECOTRY OF YOUR CHOICE>
```

#### Run install script
This will create a directory named `openrelik` in the current working directory. Everything that is needed is contained in this directory.

**Optional: inspect the script before executing it**
```shell
cat install.sh
```
**Run the script, this will install OpenRelik in the current working directory**
```shell
bash install.sh
cd openrelik
```

### 3. Create OAuth credentials in a Google Cloud project
https://developers.google.com/workspace/guides/create-credentials#oauth-client-id

Steps:
1. Create a new GCP project, or use an existing one
2. Navigate to "APIs & Services > Credentials"
3. Click "+ CREATE CREDENTIALS" > OAuth client ID
4. Select"Web application" as the Application type
5. Name it "OpenRelik Localhost" or to whatever you want (it doesn't matter)
6. In "Authorized redirect URIs" click "+ ADD URI"
7. Enter "http://localhost:8710/auth"
8. Click "SAVE"

On the right you will have details for your new credentials. The important ones are:
* Client ID
* Client secret

You need both of these in the next step.

#### Edit config/settings.toml
Configure the Google OAuth credentials that was created in the previous step.

```shell
client_id = "<CLIENT ID FROM PREVIOUS STEP>"
client_secret = "<CLIENT SECRET FROM PREVIOUS STEP>"
```

Grant yourself access to the server
```shell
allowlist = ['<YOUR GMAIL ACCOUNT NAME>@gmail.com']
```

### 4. Start the system
```shell
docker compose up -d
```

### 5. Access openrelik UI
```shell
http://localhost:8711/
```

{{< callout type="info" >}}
If you want to access the API server and the generated documentation:
```shell
http://localhost:8710/api/v1/docs/
```
{{< /callout >}}
