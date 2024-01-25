# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys
import tempfile

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.cmd
import spack.util.compression as compression
from spack.cmd.common import arguments

description = "print out logs for packages"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["spec"])


def _dump_byte_stream_to_stdout(stream):
    with open(sys.stdout.fileno(), "wb") as outstream:
        line = stream.readline()
        while line:
            outstream.write(line)
            line = stream.readline()


def dump_build_log(package):
    with open(package.log_path, "rb") as f:
        _dump_byte_stream_to_stdout(f)


def logs(parser, args):
    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        tty.die("You must supply a spec.")

    if len(specs) != 1:
        tty.die("Too many specs.  Supply only one.")

    spec = spack.cmd.matching_spec_from_env(specs[0])

    if spec.installed:
        log_path = spec.package.install_log_path
    elif os.path.exists(spec.package.stage.path):
        dump_build_log(spec.package)
        return
    else:
        tty.die(f"{specs[0]} is not installed or staged")

    if not os.path.exists(log_path):
        tty.die(f"No logs are available for {specs[0]}")

    compression_ext = compression.extension_from_file(log_path)
    fstream = None
    temp_dir = None
    try:
        if not compression_ext:
            fstream = open(log_path, "rb")
        else:
            decompressor = compression.decompressor_for(log_path, extension=compression_ext)
            temp_dir = tempfile.mkdtemp(suffix=f"decompress-spack-log-{spec.name}")

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
                    fstream = open(result[0], "rb")

        _dump_byte_stream_to_stdout(fstream)
    finally:
        if fstream:
            fstream.close()
        if temp_dir:
            shutil.rmtree(temp_dir)
