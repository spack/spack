#!/usr/bin/env spack-python
"""
This script is meant to be run using:
    `spack python aggregate_logs.spack.py`
"""

import os


def find_logs(prefix, filename):
    for root, _, files in os.walk(prefix):
        if filename in files:
            yield os.path.join(root, filename)


if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser("aggregate_logs")
    parser.add_argument("output_file")
    parser.add_argument("--log", default="install_times.json")
    parser.add_argument("--prefix", required=True)

    args = parser.parse_args()

    prefixes = [p for p in args.prefix.split(":") if os.path.exists(p)]

    # Aggregate the install timers into a single json
    data = []
    for prefix in prefixes:
        time_logs = find_logs(prefix, args.log)
        for log in time_logs:
            with open(log) as fd:
                data.append(json.load(fd))

    with open(args.output_file, "w") as fd:
        json.dump(data, fd)
