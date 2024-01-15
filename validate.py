import glob
import json
import logging
import sys
from jsonschema import validate, ValidationError
from ruamel.yaml import YAML

def setup_logger():
    logger = logging.getLogger("PlexAniSync")
    return logger

def load_schema(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_mappings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        yaml = YAML(typ='safe')
        return yaml.load(f)

def validate_mappings(file_mappings, schema, logger):
    try:
        validate(file_mappings, schema)
    except ValidationError as e:
        logger.error(f"Custom Mappings validation failed!")
        logger.error(f"File: {file_mappings}, {e.message} at entry {e.instance}")
        return False
    return True

def main():
    logger = setup_logger()
    schema = load_schema('./custom_mappings_schema.json')

    success = True
    for file in glob.glob("mappings/*.yaml"):
        file_mappings = load_mappings(file)
        success = validate_mappings(file_mappings, schema, logger) and success

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
