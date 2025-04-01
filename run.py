#!/usr/bin/env python
"""The run script"""
import logging
from flywheel_gear_toolkit import GearToolkitContext
from utils.parser import parse_config
from app.tagger import tagger

# Set up logging
log = logging.getLogger(__name__)

# Define main function
def main(context: GearToolkitContext) -> None:

    
    # Get the input files
    input, T2wQC, T1wQC, FLAIRQC, ADCQC = parse_config(context)
    
    # Run the nii2dcm function
    tagger(input, T2wQC, T1wQC, FLAIRQC, ADCQC)  

# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()
        # Pass the gear context into main function defined above.
        main(gear_context)