# ProjectCreator

Create a new project by cloning a template repository.

This capability is exposed via the CLI: `python -m gutil create project <name>`.

## Requirements

- Python 3.8+
- `git` installed and on PATH
- Network access to the template repository
- For SSH URL usage, a configured GitHub SSH key

## Usage

Default template: `git@github.com:0x7C2f/vibe-coding-template.git`

```sh
python -m gutil create project my-new-app
```

With options:

```sh
# Clone a specific branch
python -m gutil create project my-new-app --branch main

# Override the template URL (e.g., prefer HTTPS)
python -m gutil create project my-new-app \
  --template https://github.com/0x7C2f/vibe-coding-template.git
```

If the target directory already exists, the command fails with an error.

## Library API

If you want to call this from Python code instead of the CLI:

```python
from gutil.ProjectCreator import ProjectCreator

creator = ProjectCreator()
path = creator.create_project("my-new-app")
print("Created at:", path)
```

Parameters:
- `name` (str): Target directory name (must not exist).
- `template_url` (str, optional): Git URL for the template.
- `branch` (str, optional): Branch to clone.

Raises:
- `ValueError` for invalid inputs.
- `RuntimeError` for clone errors (including missing git or network failures).

