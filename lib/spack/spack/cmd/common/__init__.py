##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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
