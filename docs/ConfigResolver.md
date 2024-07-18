# ConfigResolver

The `ConfigResolver` class is a utility for managing configuration data from YAML files and environment variables. It allows you to load environment variables from a `.env` file and resolve them within YAML configurations, making it easy to manage settings and sensitive data across different environments.

## Features

- Load environment variables from a `.env` file.
- Resolve environment variable placeholders in YAML files.
- Access nested configuration values using a key path.
- Handle errors gracefully with informative messages.

## Installation

1. Clone the repository or download the `config_resolver.py` file.
2. Ensure you have Python installed (version 3.6+).
3. Install the required dependencies using pip:

    ```sh
    pip install pyyaml python-dotenv
    ```

## Usage

### Initialization

Create an instance of the `ConfigResolver` class:

```py
from config_resolver import ConfigResolver

resolver = ConfigResolver()
```

### Loading and Resolving .env

Load environment variables from a .env file:

```py
resolver.load_config('.env', 'path/to/variable')
```

### Loading and Resolving config.yaml
```py
resolver.load_config('config', 'path/to/variable')
```

### Example
Given a .env file:

```sh
DATABASE_URL=mysql://user:password@localhost/dbname
```

And a config.yaml file:

```yml
database:
  url: ${DATABASE_URL}
```

```py
from config_resolver import ConfigResolver

resolver = ConfigResolver()

database_url_config = resolver.load_config('config', 'database/url')
database_url_env = resolver.load_config('.env', 'DATABASE_URL')

print(f"Database URL: {database_url_config}")
print(f"Database URL: {database_url_env}")
```

```sh
Loaded environment variables from .env
Loaded configuration from config.yaml
Accessed environment variable DATABASE_URL to mysql://user:password@localhost/dbname
Accessed variable 'database/url' with value: mysql://user:password@localhost/dbname
Database URL: mysql://user:password@localhost/dbname
```