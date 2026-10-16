# Copyright 2019-2020 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
archspec command line interface
"""

import argparse
import typing

from . import __version__ as archspec_version
from .cpu import host, why_not
from .gpu import host as gpu_host


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "archspec",
        description="archspec command line interface",
        add_help=False,
    )
    parser.add_argument(
        "--version",
        "-V",
        help="Show the version and exit.",
        action="version",
        version=f"archspec, version {archspec_version}",
    )
    parser.add_argument("--help", "-h", help="Show the help and exit.", action="help")

    subcommands = parser.add_subparsers(
        title="command",
        metavar="COMMAND",
        dest="command",
    )

    cpu_command = subcommands.add_parser(
        "cpu",
        help="archspec command line interface for CPU",
        description="archspec command line interface for CPU",
    )
    cpu_command.add_argument(
        "--why-not",
        metavar="TARGET",
        default=None,
        dest="why_not",
        help="Explain why TARGET was not selected as the host microarchitecture.",
    )
    cpu_command.set_defaults(run=cpu)

    gpu_command = subcommands.add_parser(
        "gpu",
        help="archspec command line interface for GPU",
        description="archspec command line interface for GPU",
    )
    gpu_command.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="Display detailed GPU information and exit.",
    )
    gpu_command.set_defaults(run=gpu)

    return parser


def cpu(args) -> int:
    """Run the `archspec cpu` subcommand."""
    if args.why_not is not None:
        print(why_not(args.why_not))
        return 0
    try:
        print(host())
    except FileNotFoundError as exc:
        print(exc)
        return 1
    return 0


def gpu(args) -> int:
    """Run the `archspec gpu` subcommand."""
    try:
        gpus = gpu_host()
    except Exception as exc:  # pylint: disable=broad-except
        print(exc)
        return 1

    if not gpus:
        print("No GPUs detected.")
        return 0

    num_gpus = len(gpus)
    print(f"Detected {num_gpus} GPU(s).\n")
    for i in range(num_gpus):
        print(f"GPU {i}:")
        if args.verbose:
            print(gpus[i].detailed_string())
        else:
            print(gpus[i])
        if i < (num_gpus - 1):
            print()

    return 0


def main(argv: typing.Optional[typing.List[str]] = None) -> int:
    """Run the `archspec` command line interface."""
    parser = _make_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code

    if args.command is None:
        parser.print_help()
        return 0

    return args.run(args)
