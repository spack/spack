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
from spack import *
import os


def compile_c_and_execute(source_file, include_flags, link_flags):
    """Compile C @p source_file with @p include_flags and @p link_flags,
    run and return the output.
    """
    cc = which('cc')
    flags = include_flags
    flags.extend([source_file])
    cc('-c', *flags)
    name = os.path.splitext(os.path.basename(source_file))[0]
    cc('-o', "check", "%s.o" % name,
       *link_flags)

    check = Executable('./check')
    return check(return_output=True)


def compare_output(current_output, blessed_output):
    """Compare blessed and current output of executables."""
    if not (current_output == blessed_output):
        print("Produced output does not match expected output.")
        print("Expected output:")
        print('-' * 80)
        print(blessed_output)
        print('-' * 80)
        print("Produced output:")
        print('-' * 80)
        print(current_output)
        print('-' * 80)
        raise RuntimeError("Ouput check failed.",
                           "See spack_output.log for details")


def compare_output_file(current_output, blessed_output_file):
    """Same as above, but when the blessed output is given as a file."""
    with open(blessed_output_file, 'r') as f:
        blessed_output = f.read()

    compare_output(current_output, blessed_output)
