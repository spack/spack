# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.cmd.common import print_module_placeholder_help, arguments

description = "add package to environment using `module load`"
section = "modules"
level = "short"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
       message with -h. """
    arguments.add_common_arguments(
        subparser, ['recurse_dependencies', 'specs'])


def load(parser, args):
    print_module_placeholder_help()
