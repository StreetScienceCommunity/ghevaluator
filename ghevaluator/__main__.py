#!/usr/bin/env python3

import argparse
import ghevaluator

from pathlib import Path


def main(argv=None):
    """
    The main function

    Compare one history to a reference workflow or history, or several histories listed in a CSV file,
    and write the reports.
    """
    parser = argparse.ArgumentParser(description='Compare Galaxy histories to a reference workflow or history and generate JSON, HTML and Markdown reports')
    parser.add_argument('-u', '--history_url', help="URL to Galaxy history")
    reference = parser.add_mutually_exclusive_group()
    reference.add_argument('-w', '--workflow_url', help="URL to reference workflow: a workflow file (.ga) or a Galaxy workflow link")
    reference.add_argument('-r', '--reference_history_url', help="URL to reference Galaxy history")
    parser.add_argument('-c', '--csv', type=Path, help="CSV file with several histories to evaluate, with columns 'student name', 'stud hist id', 'ref hist id' and optional 'tutorial name' (ids or URLs)")
    parser.add_argument('-g', '--galaxy_url', default=ghevaluator.DEFAULT_GALAXY_URL, help="Galaxy server of the API key, also used for history ids in the CSV file. The API key is only sent to this server (default: https://usegalaxy.eu)")
    parser.add_argument('-a', '--apikey', help="Galaxy API key of an account on the --galaxy_url server, needed for histories shared with a specific account, not for published histories or histories shared via link")
    parser.add_argument('-o', '--output', help="Path to output folder (default: current folder)", type=Path, default=Path('.'))
    args = parser.parse_args(argv)

    if args.csv:
        if args.history_url or args.workflow_url or args.reference_history_url:
            parser.error("use either --csv or --history_url with a reference")
        ghevaluator.ghevaluator_batch(args.csv, Path(args.output), args.apikey, args.galaxy_url)
    elif args.history_url and (args.workflow_url or args.reference_history_url):
        ghevaluator.ghevaluator(
            args.history_url,
            args.workflow_url or args.reference_history_url,
            args.apikey,
            Path(args.output),
            ref_type='workflow' if args.workflow_url else 'history',
            galaxy_url=args.galaxy_url)
    else:
        parser.error("give --history_url and a reference (--workflow_url or --reference_history_url), or --csv")


if __name__ == "__main__":
    main()
