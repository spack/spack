# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tempfile
import time

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.cmd
import spack.environment as ev
import spack.util.compression as compression
from spack.cmd.common import arguments

description = "print out logs for packages"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "--continuous", action="store_true", help="for stage logs, poll for new content"
    )

    arguments.add_common_arguments(subparser, ["spec"])


def dump_build_log(path, continuous):
    with open(path, "r") as fstream:
        line = fstream.readline()
        while True:
            if line:
                print(line.strip())
            elif continuous:
                time.sleep(0.2)
            else:
                break
            line = fstream.readline()


def log(parser, args):
    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        tty.die("You must supply a spec.")

    if len(specs) != 1:
        tty.die("Too many specs.  Supply only one.")

    env = ev.active_environment()

    if env:
        spec = spack.cmd.matching_spec_from_env(specs[0])
    else:
        spec = specs[0].concretized()

    if spec.installed:
        log_path = spec.package.install_log_path
    elif os.path.exists(spec.package.stage.path):
        dump_build_log(spec.package.log_path, args.continuous)
        return
    else:
        tty.die(f"{specs[0]} is not installed or staged")

    if not os.path.exists(log_path):
        tty.die(f"No logs are available for {specs[0]}")

    compression_ext = compression.extension_from_file(log_path)
    fstream = None
    try:
        if not compression_ext:
            fstream = open(log_path, "r")
        else:
            decompressor = compression.decompressor_for(log_path, extension=compression_ext)
            with tempfile.TemporaryDirectory() as temp_dir:
                with fs.working_dir(temp_dir):
                    decompressor(log_path)
                    result = os.listdir(".")
                    if len(result) < 1:
                        tty.die(
                            f"Detected compressed log for {specs[0]},"
                            f" but could not decompress {log_path}"
                        )
                    elif len(result) > 1:
                        tty.die(f"Compressed log {log_path} expanded to more than 1 file")
                    else:
                        fstream = open(result[0], "r")

        line = fstream.readline()
        while line:
            print(line.strip())
            line = fstream.readline()
    finally:
        if fstream:
            fstream.close()
