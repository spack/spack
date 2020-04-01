# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.paths
from llnl.util import tty


shell_init_instructions = [
    "To initialize spack's shell commands:",
    "",
    "    # for bash and zsh",
    "    . %s/setup-env.sh" % spack.paths.share_path,
    "",
    "    # for csh and tcsh",
    "    setenv SPACK_ROOT %s" % spack.paths.prefix,
    "    source %s/setup-env.csh" % spack.paths.share_path, ""
]


def print_module_placeholder_help():
    """
    For use by commands to tell user how to activate shell support.
    """
    msg = [
        "This command requires spack's shell integration.", ""
    ] + shell_init_instructions + [
        "This exposes a 'spack' shell function, which you can use like",
        "    $ spack load package-foo", "",
        "Running the Spack executable directly (for example, invoking",
        "./bin/spack) will bypass the shell function and print this",
        "placeholder message, even if you have sourced one of the above",
        "shell integration scripts."
    ]
    tty.msg(*msg)
