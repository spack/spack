# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function
import argparse
import os
import tempfile

import spack.cmd
from spack.util.package_hash import package_content

from llnl.util.filesystem import working_dir


def setup_parser(subparser):
    subparser.add_argument(
        'files', nargs=argparse.REMAINDER, help="specific files to check")


def package_ast_check(parser, args):
    temp = tempfile.mkdtemp()

    file_list = args.files
    if file_list:
        file_list = [os.path.abspath(os.path.realpath(p)) for p in file_list]
    else:
        file_list = spack.cmd.changed_files()

    all_pkg_names = spack.repo.all_package_names()

    for pkg_name in all_pkg_names:
        if spack.repo.path.filename_for_package_name(pkg_name) in file_list:
            package_content(pkg_name)
