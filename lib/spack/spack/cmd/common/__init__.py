# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.paths
from llnl.util import tty


def print_module_placeholder_help():
    """
    For use by commands to tell user how to activate shell support.
    """
    tty.msg("This command requires spack's shell integration.", "",
            "To initialize spack's shell commands, you must run one of",
            "the commands below.  Choose the right command for your shell.",
            "", "For bash and zsh:",
            "    . %s/setup-env.sh" % spack.paths.share_path, "",
            "For csh and tcsh:",
            "    setenv SPACK_ROOT %s" % spack.paths.prefix,
            "    source %s/setup-env.csh" % spack.paths.share_path, "",
            "This exposes a 'spack' shell function, which you can use like",
            "    $ spack load package-foo", "",
            "Running the Spack executable directly (for example, invoking",
            "./bin/spack) will bypass the shell function and print this",
            "placeholder message, even if you have sourced one of the above",
            "shell integration scripts.")
