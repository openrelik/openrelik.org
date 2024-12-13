+++
title = 'Design Proposal: Transition to Semantic Versioning'
linkTitle = 'Versioning'
date = 2024-12-13T10:16:18+01:00
draft = false
+++

This document proposes a transition from the current calendar versioning (CalVer) scheme to Semantic Versioning (SemVer) for the OpenRelik project. This change addresses limitations of the current scheme in managing dependencies and communicating changes between project components. This proposal details the motivation, implementation, and impact of this transition.

**2. Current State**

The OpenRelik project currently employs CalVer. Releases are identified by a date-based identifier (YYYY.MM.DD). This approach offers temporal context but fails to express the nature and scope of changes between releases. This lack of semantic information complicates dependency management, particularly between the `openrelik-server`, `openrelik-ui`, `openrelik-worker-common`, and various worker repositories (e.g., `openrelik-worker-example1`).

**3. Problem Statement**

CalVer lacks the granularity necessary to express compatibility between components. It does not differentiate between backward-compatible additions, bug fixes, and breaking changes. This absence of semantic information creates challenges:

*   **Dependency Tracking:** Determining compatible component versions requires manual inspection of release notes.
*   **Automated Deployment:** Automated deployment pipelines cannot reliably determine compatible versions based on the version identifier.
*   **Communication of Change Impact:** Users lack a concise method to understand the impact of upgrading to a new version.

**4. Proposed Solution: Semantic Versioning**

This proposal advocates for adoption of SemVer 2.0.0. SemVer uses a three-part version number: MAJOR.MINOR.PATCH.

*   **MAJOR:** Incremented for incompatible API changes.
*   **MINOR:** Incremented for backward-compatible additions of functionality.
*   **PATCH:** Incremented for backward-compatible bug fixes.

This scheme provides explicit information about the nature of changes. It facilitates automated dependency management and improves communication about release impact.

**5. Implementation Details**

**5.1 Version Numbering:**

The initial release under SemVer will be 0.1.0 for all repositories. This signifies a stable release and a clear transition point. Subsequent releases will adhere strictly to SemVer rules.

**5.2 Dependency Management:**

Component dependencies will be expressed using version ranges. This allows for flexibility while ensuring compatibility. Examples:

*   `^1.2.3`: Compatible with 1.2.3 and any subsequent 1.x.x releases, but not 2.0.0.
*   `~1.2.3`: Compatible with 1.2.x releases, but not 1.3.0.
*   `>=1.0.0 <2.0.0`: Compatible with 1.x.x releases.

**5.3 Compatibility Matrix:**

A compatibility matrix will document compatible versions between components. This matrix will be maintained and updated with each release.

**5.4 Tooling:**

Standard version control tools (e.g., Git) and package managers (e.g., npm, pip) will be used to manage and track versions. Automation scripts will enforce SemVer compliance during the release process.

**5.5 API Versioning:**

For significant API changes that cannot maintain backward compatibility, API versioning (e.g., /v1/, /v2/ in API endpoints) will be employed in addition to SemVer. This allows simultaneous support for multiple API versions.

**6. Transition Plan**

1.  **Documentation Update:** Update project documentation to reflect the new versioning scheme.
2.  **Tooling Configuration:** Configure build and deployment pipelines to enforce SemVer.
3.  **Initial Release:** Release all components at version 0.1.0.
4.  **Communication:** Communicate the change to users and developers.

**7. Impact Assessment**

**7.1 Positive Impacts:**

*   Improved dependency management.
*   Enhanced communication regarding release impact.
*   Facilitation of automated deployments.
*   Increased project maintainability.

**7.2 Negative Impacts:**

*   Initial overhead for implementation and transition.
*   Potential need for updates to existing integrations.

**8. Conclusion**

Transitioning to SemVer offers significant advantages for the OpenRelik project. It addresses current limitations in version management and sets a solid foundation for future development. This proposal recommends immediate adoption of SemVer.
