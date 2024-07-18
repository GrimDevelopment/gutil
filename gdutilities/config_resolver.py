import yaml
from dotenv import dotenv_values

class ConfigResolver:
    def __init__(self):
        self.env_vars = {}

    def load_env_variables(self, env_file):
        """Load environment variables from a specified .env file."""
        try:
            self.env_vars = dotenv_values(env_file)
            print(f"Loaded environment variables from {env_file}")
        except Exception as e:
            print(f"Error loading environment variables from {env_file}: {e}")

    def env_constructor(self, loader, node):
        """Custom constructor for !ENV tag to handle environment variable placeholders in YAML."""
        value = loader.construct_scalar(node)
        if value.startswith('${') and value.endswith('}') and value[2:-1] in self.env_vars:
            resolved_value = self.env_vars[value[2:-1]]
            print(f"Resolved environment variable {value} to {resolved_value}")
            return resolved_value
        else:
            print(f"Environment variable {value} not found in loaded environment variables")
            return value

    def resolve_env_variables(self, data):
        """Recursively resolve !ENV placeholders in YAML data."""
        if isinstance(data, dict):
            return {key: self.resolve_env_variables(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.resolve_env_variables(item) for item in data]
        else:
            return data

    def load_config(self, source, variable_path):
        """Resolve config or env variables and access nested keys."""
        try:
            if source == 'config':
                # Load YAML config
                with open('config.yaml', 'r') as file:
                    config = yaml.load(file, Loader=yaml.Loader)
                print(f"Loaded configuration from config.yaml")

                # Resolve environment variables in the loaded YAML data
                resolved_config = self.resolve_env_variables(config)
                print(f"Resolved environment variables in config.yaml")

                # Access the nested variable using the variable_path
                keys = variable_path.split('/')
                value = resolved_config
                for key in keys:
                    if key in value:
                        value = value[key]
                    else:
                        raise KeyError(f"Key '{key}' not found in the configuration path '{variable_path}'")
                print(f"Accessed variable '{variable_path}' with value: {value}")
                return value
            else:
                # Load environment variables from the specified .env file
                self.load_env_variables(source)

                # Access the nested variable using the variable_path
                keys = variable_path.split('/')
                value = self.env_vars
                for key in keys:
                    if key in value:
                        value = value[key]
                    else:
                        raise KeyError(f"Key '{key}' not found in the environment variables path '{variable_path}'")
                print(f"Accessed environment variable '{variable_path}' with value: {value}")
                return value
        except KeyError as e:
            print(f"Key error: {e}")
            raise
        except Exception as e:
            print(f"Error loading configuration or environment variable: {e}")
            raise