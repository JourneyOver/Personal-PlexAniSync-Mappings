import glob
import json
import logging
import sys
from typing import List
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from ruamel.yaml import YAML
import requests

# Initialize logger
logger = logging.getLogger("PlexAniSync")

# YAML and schema constants
yaml = YAML(typ='safe')
schema_url = "https://raw.githubusercontent.com/RickDB/PlexAniSync/master/custom_mappings_schema.json"
local_schema_path = './custom_mappings_schema.json'

# Try to load the schema from local file or remote URL
def load_schema() -> dict:
    """Load schema from local file or fetch from remote if not found."""
    try:
        with open(local_schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            response = requests.get(schema_url)
            response.raise_for_status()
            schema = response.json()

            # Save the fetched schema locally
            with open(local_schema_path, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=4)
            return schema
        except requests.RequestException as e:
            logger.error(f"Failed to fetch schema from {schema_url}: {e}")
            sys.exit(1)

def validate_file_mappings(file_path: str, schema: dict) -> bool:
    """Validate the mappings in a file against the schema and check for duplicates."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_mappings = yaml.load(f)

        # Validate data against the schema
        validate(file_mappings, schema)

        # Check for duplicate titles
        titles: List[str] = []
        for entry in file_mappings["entries"]:
            title = entry["title"].lower()
            if title in titles:
                raise ValidationError(f"Duplicate title found: {entry['title']}", instance=entry)
            titles.append(title)

        return True  # Validation successful
    except ValidationError as e:
        logger.error(f"Custom Mappings validation failed for {file_path}!")
        logger.error(f"{e.message} at entry {e.instance}")
        return False  # Validation failed

def main():
    """Main function to process all YAML files."""
    schema = load_schema()
    success = True

    for file in glob.glob("mappings/*.yaml"):
        if not validate_file_mappings(file, schema):
            success = False

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
