import flywheel
import json
import os


def load_config(file_path: str) -> dict:
    """Load the JSON configuration file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error reading config file: {e}")


def initialize_flywheel_client(config: dict) -> flywheel.Client:
    """Initialize the Flywheel client using the API key from the config."""
    try:
        api_key = config['inputs']['api-key']['key']
        return flywheel.Client(api_key=api_key)
    except KeyError:
        raise RuntimeError("API key not found in the configuration file.")


def process_nifti(file_obj, modality: str):
    """
    Process a NIfTI file object, adding a 'read' tag if necessary.

    Args:
        file_obj: Flywheel file object.
        modality: The modality being processed (e.g., T2w, T1w).
    """
    # Check if the file is a NIfTI file
    if file_obj.type == 'nifti':
        if not file_obj.tags:
            file_obj.add_tag('read')
            print(file_obj.name, f"'read' tag added for {modality}")
        else:
            # Add 'read' tag only if none of the QC tags are present
            if not any(tag in file_obj.tags for tag in ['read', 'QC_unclear', 'QC_failed', 'QC_passed']):
                file_obj.add_tag('read')
                print(file_obj.name, f"'read' tag added for {modality}")
            else:
                print(file_obj.name, "QC tag already present")
    else:
        print(file_obj.name, "is not a NIfTI file. Skipping.")


def tagger(T2wQC: bool, T1wQC: bool, FLAIRQC: bool, ADCQC: bool):
    """
    Tag files in Flywheel for visual QC tasks.
    """
    config_path = '/flywheel/v0/config.json'
    config = load_config(config_path)

    # Initialize Flywheel client
    fw = initialize_flywheel_client(config)

    # Get the input file object
    input_file_id = config['inputs']['input']['hierarchy']['id']
    file_obj = fw.get(input_file_id)
    print("input_file_id is:", input_file_id)

    # Process each QC type
    if T2wQC and 'T2' in file_obj.label and 'Align' not in file_obj.label and 'Segmentation' not in file_obj.label:
        process_nifti(file_obj, "T2w")
    if T1wQC and 'T1' in file_obj.label:
        process_nifti(file_obj, "T1w")
    if FLAIRQC and 'FLAIR' in file_obj.label:
        process_nifti(file_obj, "FLAIR")
    if ADCQC and 'ADC' in file_obj.label:
        process_nifti(file_obj, "ADC")