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

import os
import os.path

import llnl.util.lang
import llnl.util.tty as tty
import spack.util.executable

#: Module scope variable that enable/disable the hook
enabled = False

#: The strip executable, if found
strip = spack.util.executable.which('strip')


def post_install(spec):
    # Exit early if the hook is not enabled
    if not enabled:
        return

    for root, _, files in os.walk(spec.prefix):
        # The .spack directory is not accounted for
        if '.spack' in root or not files:
            continue

        # Construct absolute paths and strip only the binary files
        abs_filenames = [os.path.join(root, file) for file in files]
        for binary_file in filter(is_binary, abs_filenames):
            tty.debug('[STRIP BINARIES] {0}'.format(binary_file))
            try:
                strip(binary_file)
            except Exception as e:
                tty.debug('[STRIP BINARIES FAILED] {0}'.format(str(e)))


def is_binary(file):
    """Returns true if a file is binary, False otherwise
    Args:
        file: file to be tested
    Returns:
        True or False
    """
    m_type, _ = mime_type(file)
    if m_type == 'application':
        return True

    return False


@llnl.util.lang.memoized
def mime_type(file):
    """Returns the mime type and subtype of a file.
    Args:
        file: file to be analyzed
    Returns:
        Tuple containing the MIME type and subtype
    """
    file_cmd = spack.util.executable.Executable('file')
    output = file_cmd('-b', '--mime-type', file, output=str, error=str)
    tty.debug('[MIME_TYPE] {0} -> {1}'.format(file, output.strip()))
    return tuple(output.strip().split('/'))
