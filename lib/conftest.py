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

import imp
import os.path


##########
# Source bin file as if bin/spack was invoked directly
##########


def spack_bin_path_form_this_file():
    t = __file__
    t = os.path.realpath(os.path.expanduser(t))
    t = os.path.dirname(os.path.dirname(t))
    t = os.path.join(t, 'bin', 'spack')
    return t


# Compute the absolute path of the directory where the script resides
SPACK_BIN_PATH = spack_bin_path_form_this_file()
with open(SPACK_BIN_PATH) as f:
    imp.load_source('__spack_bin', SPACK_BIN_PATH, f)
