---
title: "CLI user guide"
---

This guide describes how to configure and use the OpenRelik command-line interface (CLI) to manage files, folders, and run forensic workflows.

## Installation

### macOS

Install using Homebrew:

```bash
brew tap openrelik/openrelik-cli
brew install openrelik-cli
```

### Linux

Download the binary from GitHub:
[https://github.com/openrelik/openrelik-cli/releases](https://github.com/openrelik/openrelik-cli/releases)

---

## Global Flags

These flags modify output behavior for all commands:

*   `--format`: Set output styling to `human`, `json`, or `verbose`.
*   `--quiet`, `-q`: Suppress all output.

---

## Authentication (`auth`)

Configure credentials and active server connections. The CLI prioritizes `OPENRELIK_SERVER_URL` and `OPENRELIK_API_KEY` environment variables over local configuration settings.

*   `auth login`: Prompt for server URL and API key, saving them to `~/.openrelik/config.json`.
*   `auth status`: Show connection status and the active server.
*   `auth list`: List all configured servers.
*   `auth switch`: Change the active server.

### Examples

```bash
# Start interactive login
openrelik auth login

# Run commands without storing credentials locally
export OPENRELIK_SERVER_URL=http://localhost:8710
export OPENRELIK_API_KEY=your-api-key
```

---

## User Profiles (`user`)

Inspect user account details.

*   `user me`: Show metadata for the currently authenticated user profile.

### Example

```bash
openrelik user me --format json
```

---

## Folder Management (`folder`)

Organize files in hierarchical directories.

*   `folder list [PARENT_ID]`: List root folders. If you provide a parent ID, list subfolders inside that parent.
*   `folder create <NAME>`: Create a new folder. Use `--parent <ID>` to create a subfolder.
*   `folder mirror <DIR>`: Recreate a local directory structure on the server.

### Examples

```bash
# Create a root folder
openrelik folder create "Investigation 2026"

# Create a subfolder under folder ID 12
openrelik folder create "Evidence" --parent 12
```

---

## File Management (`file`)

Upload, download, and inspect forensic files.

*   `file list <FOLDER_ID>`: List all files in the specified folder.
*   `file info <FILE_ID>`: Return file metadata including size, hashes, and MIME type.
*   `file upload <LOCAL_PATH>`: Upload a local file. Use `--folder <ID>` to choose the target folder.
*   `file download <FILE_ID>`: Download a file. Use `--output-dir` to choose the destination.

### Examples

```bash
# Upload a disk image to folder 42
openrelik file upload /path/to/image.dd --folder 42

# Download file 105 to a custom directory
openrelik file download 105 --output-dir /tmp/downloads
```

---

## Worker Management (`worker`)

Inspect processing workers.

*   `worker list`: List registered workers and update the local cache at `~/.openrelik/workers_cache.json`.

### Example

```bash
openrelik worker list
```

---

## Templates and Workflows (`template`, `workflow`)

Manage and execute forensic pipelines.

*   `template list`: List available workflow templates.
*   `workflow create`: Create a workflow. Requires `--file <ID>` and `--template <ID>`. Use `--run` to execute immediately.
*   `workflow info <ID>`: Display workflow structure and configuration.
*   `workflow status <ID>`: Show current execution status.
*   `workflow run <ID>`: Start a created workflow.

### Example

```bash
# Create and start a workflow from file 10 using template 5
openrelik workflow create --file 10 --template 5 --run
```

---

## Dynamic Worker Execution (`run`)

Run workers on files. The CLI reads the local worker cache to generate subcommands dynamically. Inputs can be server-side file IDs or local paths, which the CLI uploads automatically before running the worker.

*   `run <worker_name> <input>`: Run a specific worker on an input.
*   Use `--then` to chain workers sequentially (passing output from one to the next).
*   Use `--and` to run workers in parallel.
*   Use `--dry-run` to output the generated JSON workflow specification without executing it.

### Examples

```bash
# Run the strings worker on file 100
openrelik run strings 100

# Run strings on a local file (uploads automatically)
openrelik run strings suspicious.exe

# Chain strings to grep
openrelik run strings --then grep --regex "password" 100

# Preview the generated workflow JSON spec without running
openrelik run strings --then grep --regex "password" 100 --dry-run
```

---

## AI Agent Skill Integration (`skill`)

Install specification files for AI assistants.

*   `skill install [dir]`: Query registered workers dynamically from the active OpenRelik server and generate a customized `SKILL.md` file. This tailors the skill capabilities directly to your server's available workers so AI agents can discover and run them.
*   Use `--harness` to target frameworks (`generic`, `codex`, `gemini`, `claude`, `opencode`, `pi`, `copilot`).
*   Use `--local` to install the skill in the current project directory.

### Examples

```bash
# Install the skill to the default global directory for Gemini (~/.gemini/skills/openrelik/SKILL.md)
openrelik skill install --harness gemini

# Install the skill locally in the current folder structure
openrelik skill install --local --harness generic
```
