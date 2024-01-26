# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys
import tempfile

import llnl.util.filesystem as fs

import spack.cmd
import spack.util.compression as compression
from spack.cmd.common import arguments

description = "print out logs for packages"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["spec"])


def _dump_byte_stream_to_stdout(instream):
    if sys.platform == "win32":
        # https://docs.python.org/3/library/sys.html#sys.stdout unconditionally
        # recommends using .buffer to write binary data to sys.stdout, but
        # https://docs.python.org/3/library/io.html#io.TextIOBase.buffer claims
        # it is not available in all implementations, so only try accessing it
        # on Windows, where stdout.fileno() is not useful
        try:
            outstream = sys.stdout.buffer
        except AttributeError:
            raise spack.main.SpackCommandError(
                "This command cannot be invoked in a"
                " context where stdout is not accessible"
                f" as a binary stream (stdout = {type(sys.stdout)})"
            )
    else:
        outstream = os.fdopen(sys.stdout.fileno(), "wb", closefd=False)

    shutil.copyfileobj(instream, outstream)


def dump_build_log(package):
    with open(package.log_path, "rb") as f:
        _dump_byte_stream_to_stdout(f)


def _logs(cmdline_spec, concrete_spec):
    if concrete_spec.installed:
        log_path = concrete_spec.package.install_log_path
    elif os.path.exists(concrete_spec.package.stage.path):
        dump_build_log(concrete_spec.package)
        return
    else:
        raise spack.main.SpackCommandError(f"{cmdline_spec} is not installed or staged")

    if not os.path.exists(log_path):
        raise spack.main.SpackCommandError(f"No logs are available for {cmdline_spec}")

    compression_ext = compression.extension_from_file(log_path)
    fstream = None
    temp_dir = None
    try:
        if not compression_ext:
            fstream = open(log_path, "rb")
        else:
            decompressor = compression.decompressor_for(log_path, extension=compression_ext)
            temp_dir = tempfile.mkdtemp(suffix=f"decompress-spack-log-{concrete_spec.name}")

            with fs.working_dir(temp_dir):
                decompressor(log_path)
                result = os.listdir(".")
                if len(result) < 1:
                    raise spack.main.SpackCommandError(
                        f"Detected compressed log for {cmdline_spec},"
                        f" but could not decompress {log_path}"
                    )
                elif len(result) > 1:
                    raise spack.main.SpackCommandError(
                        f"Compressed log {log_path} expanded to more than 1 file"
                    )
                else:
                    fstream = open(result[0], "rb")

        _dump_byte_stream_to_stdout(fstream)
    finally:
        if fstream:
            fstream.close()
        if temp_dir:
            shutil.rmtree(temp_dir)


def logs(parser, args):
    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        raise spack.main.SpackCommandError("You must supply a spec.")

    if len(specs) != 1:
        raise spack.main.SpackCommandError("Too many specs. Supply only one.")

    concrete_spec = spack.cmd.matching_spec_from_env(specs[0])

    _logs(specs[0], concrete_spec)
