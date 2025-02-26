+++
title = 'Changelog'
date = 2025-02-26
draft = false
+++

### 0.5.0

{{< callout type="info" >}}
We are moving to semantic versioning from this release in order to better track compatibility aross all components.
{{< /callout >}}

**Server**

- Added a health check endpoint for service monitoring.
- Implemented a CLI command to create and manage user API keys.
- Added an importer to ingest files from Google Cloud Storage.
- Updated several dependencies, including python-jose and cryptography.
- Improved Workflow API documentation.
- Fixed an authorization bug in the workflow API.
- Refactored LLM summarization and added related unit tests.

**UI**

This release includes UI/UX improvements, API refinements, and dependency updates. AI summary prompt display was added, and file summary cards were visually improved. Cloud disk functionality was removed. Workflow tree UI and controls were also enhanced. The file size limit for GenAI processing was adjusted.

Highlights:

- Added AI summary prompt display and improved visuals.
- Adjusted file summary card appearance and functionality.
- Removed cloud disk functionality.
- Improved workflow tree UI and controls.
- Updated various dependencies, including Vite.
- Adjusted file size limit for GenAI processing.
- Refined API endpoints for consistency.

### 2024.12.12

This release improves Celery metrics with queue length and dynamic labels, optimizes folder API responses with a compact schema, updates the python-multipart dependency, and adds a Prometheus metrics exporter for Celery. It also introduces a new metrics dashboard for monitoring tasks, including detailed metrics like completion time, failure rate, and resource usage. The dashboard features auto-refresh and dynamic resolution.

**Server**

- Added queue length and dynamic labels to Celery metrics.
- Implemented a compact schema for folder API responses, reducing size.
- Integrated a Prometheus exporter to collect Celery metrics.

**UI**

- Added a new dashboard for visualizing task-related metrics.
- Implemented auto-refresh and dynamic resolution for the metrics dashboard.
- Improved task monitoring with metrics for completion time, failure rate, and resource usage.

### 2024.11.27

This release introduces role-based access control, folder sharing, improved file handling, and administrative tools. It also includes database improvements, extended JWT expiration, and optimizations for file listings. Several bug fixes and refactoring efforts improve stability and maintainability. Chunked file uploads and refresh token support are also added.

**Server**

- Implemented role-based access control (RBAC) for granular resource management.
- Added folder sharing and group management features.
- Optimized file listing responses for folders to reduce data transfer.
- Extended JWT access token expiration time.
- Added an admin command to fix file and folder ownership.
- Improved database initialization robustness.

**UI**

- Improved task configuration display and file details view.
- Enhanced file display in task results and workflow tree.
- Implemented folder sharing with access control.
- Added chunked, resumable file uploads.
- Improved CSRF token handling and login redirects.
- Added refresh token support.
