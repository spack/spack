# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.concretize import NoBuildError
from spack.util.module_cmd import load_module, module
from spack.util.prefix import Prefix


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

    canonical_names = {
        'gcc': 'GNU',
        'cce': 'CRAY',
        'intel': 'INTEL',
    }

    @property
    def modname(self):
        return "cray-libsci/{0}".format(self.version)

    @property
    def prefix(self):
        cname = self.canonical_names[self.compiler.name]
        libsci_module = module("show", self.modname).splitlines()

        for line in libsci_module:
            if "CRAY_LIBSCI_BASE_DIR" in line:
                base_dir = line.split()[-1]  # fails if dir contains ws

            if "PE_LIBSCI_GENCOMPS_{0}_x86_64".format(cname) in line:
                # the line looks like: PE_LIBSCI_GENCOMPS_GNU_x86_64 71 61 51
                # check for matching major version match
                lib_ver = [v for v in line.split()[2:]
                           if v[0] == str(self.compiler.version[0])][0]

        return Prefix(os.path.join(
            base_dir,
            cname,
            lib_ver,
            str(self.architecture.target)))

    @property
    def blas_libs(self):
        shared = True if "+shared" in self.spec else False
        compiler = self.spec.compiler.name

        if "+openmp" in self.spec and "+mpi" in self.spec:
            lib = "libsci_{0}_mpi_mp"
        elif "+openmp" in self.spec:
            lib = "libsci_{0}_mp"
        elif "+mpi" in self.spec:
            lib = "libsci_{0}_mpi"
        else:
            lib = "libsci_{0}"

        libname = lib.format(self.canonical_names[compiler].lower())

        return find_libraries(
            libname,
            root=self.prefix.lib,
            shared=shared,
            recursive=False)

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
