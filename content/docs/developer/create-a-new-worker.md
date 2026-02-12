+++
title = 'Create a new OpenRelik worker'
linkTitle = 'Create a new worker'
date = 2024-09-18
draft = false

+++

This guide will walk you through the process of creating a new OpenRelik worker using the provided template Python code. Each section below corresponds to a part of the template that requires your attention.

### Clone the worker template project
Browse to [Worker template repository](https://github.com/openrelik/openrelik-worker-template) and click the button "Use this template" button:

{{< figure src="/screenshot-github-template.png">}}

### Task Identification

```python
TASK_NAME = "your-worker-package-name.tasks.your_task_name"
```

* **`your-worker-package-name`**: Replace this with the actual name of your Python package that contains the worker code. This helps organize and identify your worker within the OpenRelik system.
* **`your_task_name`**: Replace this with a descriptive name for your specific task. This name is used for registration and routing the task within the OpenRelik queue system.

### Task Metadata

```python
TASK_METADATA = {
    "display_name": "<REPLACE_WITH_NAME_OF_THE_WORKER>",
    "description": "<REPLACE_WITH_DESCRIPTION_OF_THE_WORKER>",
    "task_config": [
        {
            "name": "<REPLACE_WITH_NAME>",
            "label": "<REPLACE_WITH_LABEL>",
            "description": "<REPLACE_WITH_DESCRIPTION>",
            "type": "<REPLACE_WITH_TYPE>",  # Types supported: text, textarea, checkbox
            "required": False,
        },
    ],
}
```

* **`display_name`**: Provide a user-friendly name for your worker. This is the name that will be displayed in the OpenRelik user interface.
* **`description`**: Write a concise description of what your worker does. This helps users understand the purpose of your worker.
* **`task_config`**: Configuration that will be rendered as a webform in the UI, and any data entered by the user will be available to the task function when executing.


### Task Function

```python
@celery.task(bind=True, name=TASK_NAME, metadata=TASK_METADATA)
def command(
    self,
    pipe_result: str = None,
    input_files: list = None,
    output_path: str = None,
    workflow_id: str = None,
    user_config: dict = None,
) -> str:
    """Run <REPLACE_WITH_COMMAND> on input files.

    Args:
        pipe_result: Base64-encoded result from the previous Celery task, if any.
        input_files: List of input file dictionaries (unused if pipe_result exists).
        output_path: Path to the output directory.
        workflow_id: ID of the workflow.
        task_config: Configuration for the task.

    Returns:
        Base64-encoded dictionary containing task results.
    """
    # ... (rest of the function code)
```

* **Function Docstring**: Update the docstring to accurately describe the command your worker will execute and how it handles input and output.
* **`base_command`**:
    * Replace `<REPLACE_WITH_COMMAND>` with the actual command you want to run.
    * Add any necessary command-line arguments or options to `base_command`.
* **`file_extension`**:
    * Replace `<REPLACE_WITH_FILE_EXTENSION>` with the appropriate file extension for your output files (e.g., `"txt"`).
* **Error Handling**:
    * Replace `<REPLACE_WITH_ERROR_STRING>` with a descriptive error message that indicates what went wrong if no output files are generated.

### Additional Considerations

* **Input Handling**: If your worker needs to process the `pipe_result` from a previous task or handle `user_config`, add the necessary logic within the `command` function.
* **Output Metadata**: The `meta` dictionary in the `task_result` function can be used to include additional metadata about the task's output, if needed.
* **Dependencies**: Make sure to install any required external libraries or tools that your worker depends on.
* **Testing**: Thoroughly test your worker to ensure it functions correctly and handles various input scenarios gracefully.

By following this guide and carefully replacing the placeholder values in the template, you can efficiently develop new OpenRelik workers to extend the platform's capabilities.

If you encounter any issues or have further questions, feel free to reach out to the OpenRelik community or development team for assistance. Happy coding!
