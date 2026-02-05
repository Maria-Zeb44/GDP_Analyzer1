import json
from typing import Dict, Any

def load_config(filepath: str = 'config.json') -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
            print(f"Config loaded from {filepath}")
            return config
    except FileNotFoundError:
        print(f"Error: Config file '{filepath}' not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{filepath}'")
        return {}

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration has required fields"""
    required = ['year', 'operation']
    missing = [key for key in required if key not in config]
    
    if missing:
        print(f"Missing required config fields: {missing}")
        return False
    
    print("Config validation passed")
    return True

# test
if __name__ == "__main__":
    print("Testing config_loader.py...")
    config = load_config()
    if config:
        print(f"Region: {config.get('region', 'Not specified')}")
        print(f"Year: {config.get('year', 'Not specified')}")
        print(f"Operation: {config.get('operation', 'Not specified')}")
        validate_config(config)