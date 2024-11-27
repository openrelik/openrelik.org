+++
title = 'Changelog'
date = 2024-11-27T16:07:41+01:00
draft = false
+++

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
