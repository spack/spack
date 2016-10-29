#############################################################################
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


class SystemBlasLapack(Package):
    """Allows one to use the system installed blas and lapack
    without contaminating the rpath with system directories

    """
    homepage = "http://www.netlib.org/lapack/"
    # Dummy url since Spack complains if I don't list something, will be
    # removed when I don't need to download a dummy file
    url      = 'https://bitbucket.org/saws/saws/get/master.tar.gz'

    version('noversions', '941a541bdf625856be18c9752249146d')

    provides('blas')
    provides('lapack')

    @property
    def blas_libs(self):
        return find_libraries(
            ['libblas'], root=self.prefix, recurse=True
        )

    @property
    def lapack_libs(self):
        return find_libraries(
            ['liblapack'], root=self.prefix, recurse=True
        )

    def install(self, spec, prefix):
        import os
        for libname in ['blas', 'lapack']:
            found   = False
            for suffix in ['.dylib', '.so', '.a']:
                lib = os.path.join('/usr', 'lib', 'lib' + libname + suffix)
                if os.path.isfile(lib):
                    try:
                        os.unlink(prefix + 'lib' + libname + suffix)
                    except:
                        pass
                    os.symlink(lib, os.path.join(prefix,
                                                 'lib' + libname + suffix))
                    found = True
                    break
            if not found:
                raise RuntimeError('Cannot locate system ' +
                                   libname + ' library'
                                   )
