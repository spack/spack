# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# This utility is used to update a config.yaml. For the pypi package,
# we currently only need to set one variable, but this may come in
# handy when we need to do something more invasive.

import argparse
import sys

import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, help="Input config.yaml", action="store", default=sys.stdin
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output config.yaml", action="store", default=sys.stdout
    )
    args = parser.parse_args()

    if args.input != sys.stdin:
        with open(args.input, "r") as f:
            in_str = f.read()
    else:
        in_str = sys.stdin.read(in_str)

    config_yaml = yaml.safe_load(in_str)
    config_yaml["config"]["install_tree"][
        "root"
    ] = "$spack_xdg_state_home/$spack_instance_id/opt/spack"

    out_str = yaml.dump(config_yaml)
    if args.output != sys.stdout:
        with open(args.output, "w") as f:
            f.write(out_str)
    else:
        sys.stdout.write(out_str)
