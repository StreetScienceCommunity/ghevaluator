#!/usr/bin/env python3

import argparse
import ghevaluator

from pathlib import Path


def main(argv=None):
    """
    The main function

    This function serves as the driver and connection between all major parts of the program:
    It does four things:

    1. Take in 4 parameters via ArgumentParser.
    2. Call different fundtions to process the parameters, and to generate two workflows.
    3. Pass the two workflows to the compare function in history_compare.py
    4. Call generate_report_file function to output the final report.
    """
    parser = argparse.ArgumentParser(description='Compare a Galaxy history to a reference workflow and generate a JSON report file')
    parser.add_argument('-u', '--history_url', help="URL to Galaxy history", required=True)
    parser.add_argument('-w', '--workflow_url', help="URL to reference workflow", required=True)
    parser.add_argument('-a', '--apikey', help="Galaxy API key for the same instance where the history is", required=True)
    parser.add_argument('-o', '--output', help="Path to output folder", type=Path)
    args = parser.parse_args()

    ghevaluator.ghevaluator(
        args.history_url,
        args.workflow_url,
        args.apikey,
        Path(args.output))
