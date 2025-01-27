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


def process_nifti(file_obj, modality: str, subject):
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
                print(f"subject {subject}, {file_obj.name}: 'read' tag added for {modality}")
            else:
                print(f"subject {subject}, {file_obj.name}: QC tag already present")
    else:
        print(file_obj.name, "is not a NIfTI file. Skipping.")


def tagger(input, T2wQC: bool, T1wQC: bool, FLAIRQC: bool, ADCQC: bool):
    """
    Tag files in Flywheel for visual QC tasks.
    """

    # Load configuration and initialize Flywheel client
    config = load_config('/flywheel/v0/config.json')
    fw = initialize_flywheel_client(config)

    # Get the input container
    hierarchy_id = config['inputs']['input']['hierarchy']['id']
    input_container = fw.get(hierarchy_id)

    # Get the subject label
    subject = fw.get(input_container.parents['subject']).label
    print("Subject is:", subject)

    for file_obj in input_container.files:
        if file_obj.type == 'nifti':
            print("file is:", file_obj.name)

            # Process each QC type
            if T2wQC and 'T2' in file_obj.name and 'Align' not in file_obj.name and 'Segmentation' not in file_obj.name:
                process_nifti(file_obj, "T2w", subject)
            if T1wQC and 'T1' in file_obj.name:
                process_nifti(file_obj, "T1w", subject)
            if FLAIRQC and 'FLAIR' in file_obj.name:
                process_nifti(file_obj, "FLAIR", subject)
            if ADCQC and 'ADC' in file_obj.name:
                process_nifti(file_obj, "ADC", subject)