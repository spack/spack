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
from spack import *
from llnl.util import filesystem
import shutil
import os


# http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
def xcopytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def xinstall_tree(src, dest, **kwargs):
    """Manually install a file to a particular location."""
    xcopytree(src, dest, **kwargs)

    for s, d in filesystem.traverse_tree(src, dest, follow_nonexisting=False):
        filesystem.set_install_permissions(d)
        filesystem.copy_mode(s, d)


class CutestSrc(Package):
    """Build system (sort of) for GALAHAD and other optimization packages."""

    homepage = "http://ccpforge.cse.rl.ac.uk/gf/project/cutest/wiki"

    # Galahad has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('1.00000', svn='http://ccpforge.cse.rl.ac.uk/svn/cutest/cutest/trunk/', revision=286)

    mainatiners = ['citibeth']
  
    def install(self, spec, prefix):
        # Google Test doesn't have a make install
        # We have to do our own install here.
        xinstall_tree('.', prefix)
