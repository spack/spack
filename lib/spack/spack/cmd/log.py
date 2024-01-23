# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.cmd
import spack.environment as ev
import spack.util.compression as compression
from spack.cmd.common import arguments

description = "print out logs for packages"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["spec"])


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
    elif os.path.exists(pkg.stage.path):
        log_path = spec.package.log_path
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
                decompressor(log_path)
                result = os.listdir(".")
                if len(result) < 1:
                    tty.die(f"Detected compressed log for {specs[0]}, but could not decompress {log_path}")
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