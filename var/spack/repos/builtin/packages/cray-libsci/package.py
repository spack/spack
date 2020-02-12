# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import LibraryList
from spack import *
import os


class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci/"
    url      = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci/"

    version("18.11.1.2")
    version("16.11.1")
    version("16.09.1")
    version('16.07.1')
    version("16.06.1")
    version("16.03.1")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    # NOTE: Cray compiler wrappers already include linking for the following
    @property
    def blas_libs(self):
        return LibraryList(os.path.join(self.prefix.lib, 'libsci.so'))

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    def install(self, spec, prefix):
        raise NoBuildError(spec)
