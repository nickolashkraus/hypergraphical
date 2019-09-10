import json
import re
import yaml


def read_json_file(filename):
    """Read a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


def write_json_file(data, filename):
    """Write a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f)


def append_file(data, filename):
    """Append a file."""
    with open(filename, 'a') as f:
        f.write(data)


def write_file(data, filename):
    """Write a file."""
    with open(filename, 'w') as f:
        f.write(data)


def read_yaml_file(filename):
    """Read a YAML file."""
    with open(filename, 'r') as f:
        return yaml.safe_load(f.read())


def write_yaml_file(data, filename):
    """Write a YAML file."""
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def slugify(string):
    string = re.sub(r'[?!\']', '', string)
    string = re.sub(r'[-\s_]+', '-', string)
    return string.lower()
