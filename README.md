# GDUtilities

GDUtilities is a Python library for managing configuration data and environment variables. It provides utilities for loading configuration settings from YAML files and directly accessing environment variables.

## Features

- Load configuration values from a YAML file.
- Directly access environment variables from a `.env` file.
- Handle errors gracefully with informative messages.

## Installation

1. Clone the repository or download the repository
2. Ensure you have Python installed (version 3.6+).
3. Install the required dependencies using pip:

```py
pip install pyyaml python-dotenv
```

## Utilities

- [Config Resolver](docs/ConfigResolver.md)  
  A utility for managing configuration data from YAML files and environment variables. It helps in loading environment variables from a `.env` file and resolving them within YAML configurations.