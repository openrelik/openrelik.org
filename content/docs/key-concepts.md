+++
title = 'Key concepts'
date = 2024-08-14T08:22:26+02:00
draft = false
weight = 2
+++

### Forensic Artifacts

* **Upload and store artifacts:** Forensic artifacts are uploaded to the platform and stored as files on the server.
* **Organise:** Users can create folders to efficiently organize and manage their uploaded forensic artifacts.

{{< figure src="/openrelik.org/screenshot-files-folders.png" caption="Example folder with files and subfolder">}}

### Workflows

* **Docker Containers:** Workflows are built using independent Docker containers, ensuring isolation and portability.
* **Communication:** These containers interact with the core system through task queue signals, enabling seamless coordination and data exchange.
* **Pipelines and Parallel Execution:** Workflows can be executed as sequential pipelines or as groups of parallel tasks, providing flexibility and optimization for various forensic investigations.
* **Intuitive User Interface:** Workflows are designed and created using an intuitive user interface, empowering users to easily define and configure their forensic analysis processes.
* **Copy and Share:** Workflows can be easily copied and shared between users, fostering collaboration and knowledge exchange.
* **Workflow Templates:** Users can create and store workflow templates, allowing for quick and efficient reuse of workflows for different evidence sets.

{{< figure src="/openrelik.org/screenshot-workflow.png" caption="Example complex workflow (non-sensical string pipeline is for demostration purpose only)">}}

### Artifact Summaries

* **LLM Integration:** The platform can connect to Large Language Model (LLM) services to generate concise and informative summaries of forensic artifacts, aiding investigators in quickly understanding their relevance and potential significance.

### Additional Considerations

* **Open-Source:** The platform is open-source, encouraging community contributions, transparency, and continuous improvement.
* **Scalability:** The system is designed to scale efficiently, accommodating growing volumes of forensic data and user activity.
data.
