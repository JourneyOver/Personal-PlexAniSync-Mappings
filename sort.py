import glob
import logging
from ruamel.yaml import YAML

def setup_logger():
    logger = logging.getLogger("PlexAniSync")
    return logger

def configure_yaml():
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False
    yaml.preserve_quotes = True
    yaml.indent(sequence=4, offset=2)
    yaml.width = 1024
    return yaml

def sort_and_save_mappings(file_path, yaml):
    with open(file_path, 'r+', encoding='utf-8') as f:
        file_mappings = yaml.load(f)
        file_mappings["entries"].sort(key=lambda entry: entry["title"].lower())
        f.seek(0)
        yaml.dump(file_mappings, f)
        f.truncate()

def main():
    logger = setup_logger()
    yaml = configure_yaml()

    for file_path in glob.glob("mappings/*.yaml"):
        sort_and_save_mappings(file_path, yaml)

if __name__ == "__main__":
    main()
