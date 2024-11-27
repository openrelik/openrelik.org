+++
title = 'Upgrade'
date = 2024-11-27
draft = false
+++

{{< callout type="warning" >}}
**Important**

If you are upgrading from a version prior to **2024.11.27** you need to take an extra step to apply
file and folder permissions with the new RBAC permission system.
```
docker compose exec openrelik-server python admin.py fix-ownership
```
{{< /callout >}}

### 1. Change version for docker containers
In your openrelik directory, edit config.env and change version for:

#### Core system
* OPENRELIK_SERVER_VERSION=<CHANGE_VERSION>
* OPENRELIK_MEDIATOR_VERSION=<CHANGE_VERSION>
* OPENRELIK_UI_VERSION=<CHANGE_VERSION>

#### Worker versions
* OPENRELIK_WORKER_STRINGS_VERSION=<CHANGE_VERSION>
* OPENRELIK_WORKER_PLASO_VERSION=<CHANGE_VERSION>
* OPENRELIK_WORKER_TIMESKETCH_VERSION=<CHANGE_VERSION>
* OPENRELIK_WORKER_HAYABUSA_VERSION=<CHANGE_VERSION>

For example, if you are upgrading to version 2024.11.27
* OPENRELIK_SERVER_VERSION=2024.11.27
* ...

### 2. Restart the system

```
$ cd /your/openrelik/directory/
$ docker compose down
$ docker compose up -d
```

### 3. Upgrade database and migrate data
For some versions there will be updates to the database schema and this need to be reflected
in your deployed database. OpenRelik uses Alembic to manage these migrations.

{{< callout type="warning" >}}
Make sure you have backed up your database before you do any migration.
{{< /callout >}}

```
$ docker exec -it openrelik-server /bin/bash
$ cd /app/openrelik/datastores/sql/
$ alembic upgrade head
```
