"""Parser module to parse gear config.json."""

from typing import Tuple
from flywheel_gear_toolkit import GearToolkitContext

def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, bool, bool, bool, bool]:
    """Parses the config info.
    Args:
        gear_context: Context.

    Returns:
        Tuple of input, dcm, out, series, desc
    """

    # input = gear_context.get_input_path("input")
    input = gear_context.get_input("input")
    T2wQC = gear_context.config.get("T2w-QC")
    T1wQC = gear_context.config.get("T1w-QC")
    FLAIRQC = gear_context.config.get("FLAIR-QC")
    ADCQC = gear_context.config.get("ADC-QC")

    return input, T2wQC, T1wQC, FLAIRQC, ADCQC


