import glob
import logging
from ruamel.yaml import YAML

# Initialize logger
logger = logging.getLogger("PlexAniSync")

# Initialize YAML with optimized settings
yaml = YAML()
yaml.default_flow_style = False
yaml.sort_base_mapping_type_on_output = False
yaml.preserve_quotes = True
yaml.indent(sequence=4, offset=2)
yaml.width = 1024

def process_yaml_file(file_path):
    """Process and sort entries in a YAML file."""
    try:
        with open(file_path, 'r+b') as f:
            file_mappings = yaml.load(f)

            # Sort the entries by title (case-insensitive)
            if "entries" in file_mappings:
                file_mappings["entries"].sort(key=lambda entry: entry["title"].lower())

                # Write the sorted mappings back to the file
                f.seek(0)
                yaml.dump(file_mappings, f)
                f.truncate()

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")

def main():
    """Main function to process all YAML files."""
    yaml_files = glob.glob("mappings/*.yaml")

    for file in yaml_files:
        process_yaml_file(file)

if __name__ == "__main__":
    main()
