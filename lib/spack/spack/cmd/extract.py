# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

import llnl.util.filesystem
import llnl.util.tty

import spack.util.compression

description = "extract/decompress archive in place"
section = "system"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "archive",
        action="store",
        type=pathlib.Path,
        help="archive (compressed or not) to be extracted",
    )


def extract(parser, args):
    archive = args.archive
    extractor = spack.util.compression.decompressor_for(str(archive))
    with llnl.util.filesystem.working_dir(archive.parent):
        out_path = extractor(str(archive))
        llnl.util.tty.info(f"Archive extracted to {archive.parent / out_path}")
