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


class Plasma(MakefilePackage):
    """Parallel Linear Algebra Software for Multicore Architectures, PLASMA is
    a software package for solving problems in dense linear algebra using
    multicore processors and Xeon Phi coprocessors. PLASMA provides
    implementations of state-of-the-art algorithms using cutting-edge task
    scheduling techniques. PLASMA currently offers a collection of routines for
    solving linear systems of equations, least squares problems, eigenvalue
    problems, and singular value problems."""

    homepage = "https://bitbucket.org/icl/plasma/"
    url      = "https://bitbucket.org/icl/plasma/downloads/plasma-17.1.tar.gz"
    hg       = "https://luszczek@bitbucket.org/icl/plasma"

    version("develop", hg=hg)
    version("17.1", "64b410b76023a41b3f07a5f0dca554e1")

    variant('shared', default=True, description="Build shared library (disables static library)")

    depends_on("blas")
    depends_on("lapack")
    depends_on("readline", when='@17.2:')

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

    patch("remove_absolute_mkl_include.patch", when="@17.1")
    patch("add_netlib_lapacke_detection.patch", when="@17.1")

    def getblaslapacklibs(self):
        if '^netlib-lapack' in self.spec:
            bl_attr = ':c,fortran'
        else:
            bl_attr = ''
        return self.spec['lapack' + bl_attr].libs + \
            self.spec['blas' + bl_attr].libs + \
            find_system_libraries(['libm'])

    def edit(self, spec, prefix):
        # copy "make.inc.mkl-gcc" provided by default into "make.inc"
        open("make.inc", "w").write(open("make.inc.mkl-gcc").read())

        make_inc = FileFilter("make.inc")

        if '~shared' in self.spec:
            make_inc.filter("-fPIC", "")  # not using fPIC

        if "^mkl" not in spec:
            make_inc.filter("-DPLASMA_WITH_MKL", "")  # not using MKL
            make_inc.filter("-DHAVE_MKL", "")         # not using MKL

        header_flags = ""
        # accumulate CPP flags for headers: <cblas.h> and <lapacke.h>
        for dep in ("blas", "lapack"):
            try:  # in case the dependency does not provide header flags
                header_flags += " " + spec[dep].headers.cpp_flags
            except Exception:
                pass

        make_inc.filter("CFLAGS +[+]=", "CFLAGS += " + header_flags + " ")

        # pass prefix variable from "make.inc" to "Makefile"
        make_inc.filter("# --*", "prefix={0}".format(self.prefix))

        # make sure CC variable comes from build environment
        make_inc.filter("CC *[?]*= * .*cc", "")

        libs = self.getblaslapacklibs().ld_flags
        if 'readline' in self.spec:
            libs += ' ' + self.spec['readline'].libs.ld_flags
            libs += ' ' + find_system_libraries(['libdl']).ld_flags
        make_inc.filter("LIBS *[?]*= * .*", "LIBS = " + libs)

    @property
    def build_targets(self):
        targets = list()

        # use $CC set by Spack
        targets.append("CC = {0}".format(self.compiler.cc))

        if "^mkl" in self.spec:
            targets.append("MKLROOT = {0}".format(env["MKLROOT"]))

        targets.append("LIBS = {0} {1} {2}".format(
                       self.getblaslapacklibs().ld_flags,
                       self.spec['readline'].libs.ld_flags,
                       find_system_libraries(['libdl']).ld_flags))
        return targets
