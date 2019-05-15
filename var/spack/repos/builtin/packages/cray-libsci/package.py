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
from spack.concretize import NoBuildError
from spack.util.module_cmd import load_module, module

class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci"
    url      = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci"

    variant("shared", default=True, description="enable shared libs")
    variant("openmp", default=False, description="link with openmp")
    variant("mpi", default=False, description="link with mpi libs")

    version('1.2.3', '0123456789abcdef0123456789abcdef')

    provides("blas")
    provides("lapack")
    provides("scalapack")
    
    def _find_gnu_lib_version(self, compiler_ver):
        """Cray-libsci names its gnu libs in the following form: gnu_XX. Depending on the
        version of the compiler the suffix will change. Note that the suffix does not directly match
        the compiler version, so instead we parse the module file and parse out the available versions and
        try to make a match with the first number."""
        ver = str(compiler_ver)
        mod = "cray-libsci/{0}".format(self.version)
        libsci_module = module("show", mod).split()
        i = libsci_module.index("PE_LIBSCI_GENCOMPS_GNU_x86_64") + 1
        while libsci_module[i] != "setenv":
            if ver == libsci_module[i][0]:
                return libsci_module[i]
            i += 1

    @property
    def blas_libs(self):

        shared = True if "+shared" in self.spec else False
        compiler = self.spec.compiler.name

        # libs use intel in their name but for others need to convert
        canonical_names = {'gcc': "gnu_{0}".format(self._find_gnu_lib_version(self.compiler.version[0])),
                           'cce': 'cray'}

        compiler = canonical_names[compiler]

        if "+openmp" in self.spec and "+mpi" in self.spec:
            lib = "libsci_{0}_mpi_mp"
        elif "+openmp" in self.spec:
            lib = "libsci_{0}_mp"
        elif "+mpi" in self.spec:
            lib = "libsci_{0}_mpi"
        else:
            lib = "libsci_{0}"

        lib = lib.format(compiler)

        return find_libraries(lib, root=self.prefix.lib, shared=shared,
                              recursive=True)

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """ Load the module into the environment for dependents """
        version = self.version
        mod = 'cray-libsci/{0}'.format(version)
        load_module(mod)

    def install(self, spec, prefix):
        raise NoBuildError(spec)
