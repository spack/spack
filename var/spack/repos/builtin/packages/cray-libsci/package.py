##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cray-libsci
#
# You can edit this file again by typing:
#
#     spack edit cray-libsci
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from spack.concretize import NoBuildError
from spack.util.module_cmd import load_module
from llnl.util.filesystem import LibraryList

class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci"
    url      = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci"

    variant("shared", default=True, description="enable shared libs")

    version('1.2.3', '0123456789abcdef0123456789abcdef')

    provides("blas")
    provides("lapack")
    provides("scalapack")

    @property
    def blas_libs(self):
        """Return the path to the library"""
        shared = True if "+shared" in self.spec else False
        compiler = self.spec.compiler.name

        if compiler == "gcc":
            compiler = "gnu"
        elif compiler == "cce":
            compiler = "cray"

        libraries = ["libsci_%s" % (compiler),
                     "libsci_%s_mp" % (compiler),
                     "libsci_%s_mpi" % (compiler),
                     "libsci_%s_mpi_mp" % (compiler)]

        return find_libraries(libraries, root=self.prefix.lib, shared=shared,
                recurse=False)

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """ Load the module into the environment for dependents """
        load_module('cray-libsci')

    def install(self, spec, prefix):
        raise NoBuildError(spec)
