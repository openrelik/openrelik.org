+++
title = 'Upgrade'
date = 2024-09-23T12:24:50+02:00
draft = false
+++

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

For example, if you are upgrading to version 2024.09.23
* OPENRELIK_SERVER_VERSION=2024.09.23
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
Make sure you have backed up your database before you fo any migration.
{{< /callout >}}

```
$ docker exec -it openrelik-server /bin/bash
$ cd /app/openrelik/datastores/sql/
$ alembic upgrade head
```
