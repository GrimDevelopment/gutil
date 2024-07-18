import yaml
from dotenv import dotenv_values

class ConfigResolver:
    def __init__(self):
        self.env_vars = {}
        self.config = None

    def load_config(self, source, variable_path):
        """Load configuration or environment variables and access nested keys."""
        try:
            if source == 'config':
                # Load YAML config
                with open('config.yaml', 'r') as file:
                    self.config = yaml.load(file, Loader=yaml.Loader)
                print(f"Loaded configuration from config.yaml")

                # Access the nested variable using the variable_path
                keys = variable_path.split('/')
                value = self.config
                for key in keys:
                    if key in value:
                        value = value[key]
                    else:
                        raise KeyError(f"Key '{key}' not found in the configuration path '{variable_path}'")
                print(f"Accessed variable '{variable_path}' with value: {value}")
                return value
            elif source == 'env':
                # Load environment variables from the .env file
                self.env_vars = dotenv_values('.env')
                print(f"Loaded environment variables from .env")

                # Access the environment variable directly
                key = variable_path
                if key in self.env_vars:
                    value = self.env_vars[key]
                    print(f"Accessed environment variable '{key}' with value: {value}")
                    return value
                else:
                    raise KeyError(f"Environment variable '{key}' not found")
            else:
                raise ValueError("Invalid source type. Must be 'config' or 'env'.")
        except KeyError as e:
            print(f"Key error: {e}")
            raise
        except Exception as e:
            print(f"Error loading configuration or environment variable: {e}")
            raise
