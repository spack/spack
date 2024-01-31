# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import gzip
import os
import shutil
import sys

import spack.cmd
import spack.util.compression as compression
from spack.cmd.common import arguments
from spack.main import SpackCommandError

description = "print out logs for packages"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["spec"])


def _dump_byte_stream_to_stdout(instream):
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
        raise SpackCommandError(f"{cmdline_spec} is not installed or staged")

    try:
        compression_ext = compression.extension_from_file(log_path)
        with open(log_path, "rb") as fstream:
            if compression_ext == "gz":
                # If the log file is compressed, wrap it with a decompressor
                fstream = gzip.open(log_path, "rb")
            elif compression_ext:
                raise SpackCommandError(
                    f"Unsupported storage format for {log_path}: {compression_ext}"
                )

            _dump_byte_stream_to_stdout(fstream)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise SpackCommandError(f"No logs are available for {cmdline_spec}") from e
        elif e.errno == errno.EPERM:
            raise SpackCommandError(f"Permission error accessing {log_path}") from e
        else:
            raise


def logs(parser, args):
    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        raise SpackCommandError("You must supply a spec.")

    if len(specs) != 1:
        raise SpackCommandError("Too many specs. Supply only one.")

    concrete_spec = spack.cmd.matching_spec_from_env(specs[0])

    _logs(specs[0], concrete_spec)
