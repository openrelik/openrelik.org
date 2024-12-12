+++
title = 'Changelog'
date = 2024-11-27T16:07:41+01:00
draft = false
+++

### 2024.12.12

This release improves Celery metrics with queue length and dynamic labels, optimizes folder API responses with a compact schema, updates the python-multipart dependency, and adds a Prometheus metrics exporter for Celery. It also introduces a new metrics dashboard for monitoring tasks, including detailed metrics like completion time, failure rate, and resource usage. The dashboard features auto-refresh and dynamic resolution.

**Server**
* Added queue length and dynamic labels to Celery metrics.
* Implemented a compact schema for folder API responses, reducing size.
* Integrated a Prometheus exporter to collect Celery metrics.

**UI**
* Added a new dashboard for visualizing task-related metrics.
* Implemented auto-refresh and dynamic resolution for the metrics dashboard.
* Improved task monitoring with metrics for completion time, failure rate, and resource usage.

### 2024.11.27

This release introduces role-based access control, folder sharing, improved file handling, and administrative tools. It also includes database improvements, extended JWT expiration, and optimizations for file listings.  Several bug fixes and refactoring efforts improve stability and maintainability. Chunked file uploads and refresh token support are also added.

**Server**
* Implemented role-based access control (RBAC) for granular resource management.
* Added folder sharing and group management features.
* Optimized file listing responses for folders to reduce data transfer.
* Extended JWT access token expiration time.
* Added an admin command to fix file and folder ownership.
* Improved database initialization robustness.

**UI**
* Improved task configuration display and file details view.
* Enhanced file display in task results and workflow tree.
* Implemented folder sharing with access control.
* Added chunked, resumable file uploads.
* Improved CSRF token handling and login redirects.
* Added refresh token support.
