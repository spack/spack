##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
"""Utilities for managing paths in Spack.
"""
import os
import re
import spack
import getpass
import tempfile

__all__ = [
    'substitute_config_variables',
    'canonicalize_path']

# Substitutions to perform
replacements = {
    'spack': spack.prefix,
    'user': getpass.getuser(),
    'tempdir': tempfile.gettempdir(),
}


def substitute_config_variables(path):
    """Substitute placeholders into paths.

    Spack allows paths in configs to have some placeholders, as follows:

    - $spack     The Spack instance's prefix
    - $user      The current user's username
    - $tempdir   Default temporary directory returned by tempfile.gettempdir()

    These are substituted case-insensitively into the path, and users can
    use either ``$var`` or ``${var}`` syntax for the variables.

    """
    # Look up replacements for re.sub in the replacements dict.
    def repl(match):
        m = match.group(0).strip('${}')
        return replacements.get(m.lower(), match.group(0))

    # Replace $var or ${var}.
    return re.sub(r'(\$\w+\b|\$\{\w+\})', repl, path)


def canonicalize_path(path):
    """Substitute config vars, expand user home, take abspath."""
    path = substitute_config_variables(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path
