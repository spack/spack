##############################################################################
# Copyright (c) 2017, Innovative Computing Laboratory
# Produced at the Innovative Computing Laboratory.
#
# Created by Piotr Luszczek, luszczek@icl.utk.edu, All rights reserved.
#
# For details, see https://github.com/spack/spack
#
##############################################################################
#
from spack import *


class Plasma(CMakePackage):
    """Parallel Linear Algebra Software for Multicore Architectures, PLASMA is
    a software package for solving problems in dense linear algebra using
    multicore processors and Xeon Phi coprocessors. PLASMA provides
    implementations of state-of-the-art algorithms using cutting-edge task
    scheduling techniques. PLASMA currently offers a collection of routines for
    solving linear systems of equations, least squares problems, eigenvalue
    problems, and singular value problems."""

    homepage = "https://bitbucket.org/icl/plasma/"
    url = "https://bitbucket.org/icl/plasma/downloads/plasma18.9.0.tar.gz"
    hg = "https://luszczek@bitbucket.org/icl/plasma"

    version("develop", hg=hg)
    version("18.9.0", sha256="753eae28ea48986a2cc7b8204d6eef646584541e59d42c3c94fa9879116b0774")

    variant("shared", default=True,
            description="Build shared library (disables static library)")

    depends_on("blas")
    depends_on("lapack")

    conflicts("atlas")  # does not have LAPACKE interface

    # missing LAPACKE features and/or CBLAS headers
    conflicts("netlib-lapack@:3.5.999")

    # clashes with OpenBLAS declarations and has a problem compiling on its own
    conflicts("cblas")

    conflicts("openblas-with-lapack")  # incomplete LAPACK implementation
    conflicts("veclibfort")

    # only GCC 4.9+ and higher have sufficient support for OpenMP 4+ tasks+deps
    conflicts("%gcc@:4.8.99", when='@:17.1')
    # only GCC 6.0+ and higher have for OpenMP 4+ Clause "priority"
    conflicts("%gcc@:5.99", when='@17.2:')

    conflicts("%cce")
    conflicts("%clang")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    def cmake_args(self):
        options = list()

        options.extend([
            "-DCMAKE_INSTALL_PREFIX=%s" % prefix,
            "-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib" % prefix,
            "-DBLAS_LIBRARIES=%s" % self.spec["blas"].libs.joined(";"),
            "-DLAPACK_LIBRARIES=%s" % self.spec["lapack"].libs.joined(";")
        ])

        options += [
            "-DBUILD_SHARED_LIBS=%s" %
            ('ON' if ('+shared' in self.spec) else 'OFF')
        ]

        return options
