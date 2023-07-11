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

    import spack.config as cfg
    import spack.environment as ev

    parser = ArgumentParser("aggregate_logs")
    parser.add_argument("output_file")
    parser.add_argument("--log")
    prefix_group = parser.add_mutually_exclusive_group()
    prefix_group.add_argument("--prefix")
    prefix_group.add_argument("--config")

    args = parser.parse_args()

    if not args.prefix:
        tmp_env = ev.create("_", init_file=args.config)
        ev.activate(tmp_env)
        prefix = cfg.get("config:install_tree:root")
    else:
        prefix = args.prefix

    # Aggregate the install timers into a single json
    time_logs = find_logs(prefix, args.log)
    data = []
    for log in time_logs:
        with open(log) as fd:
            data.append(json.load(fd))

    with open(args.output_file, "w") as fd:
        json.dump(data, fd)
