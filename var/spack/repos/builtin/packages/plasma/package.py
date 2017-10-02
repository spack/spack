##############################################################################
# Copyright (c) 2017, Innovative Computing Laboratory
# Produced at the Innovative Computing Laboratory.
#
# Created by Piotr Luszczek, luszczek@icl.utk.edu, All rights reserved.
#
# For details, see https://github.com/llnl/spack
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

    version("17.1", "64b410b76023a41b3f07a5f0dca554e1")

    version("develop", hg="https://luszczek@bitbucket.org/icl/plasma")

    depends_on("blas")
    depends_on("lapack")

    # Intel's MKL installer accesses /opt regardless of PREFIX
    conflicts("intel-mkl")
    conflicts("intel-parallel-studio")

    conflicts("atlas")  # does not have LAPACKE interface
    conflicts("netlib-lapack@:2.999")  # missing LAPACKE features
    # clashes with OpenBLAS declarations and has a problem compiling on its own
    conflicts("cblas")
    conflicts("openblas-with-lapack")  # incomplete LAPACK implementation
    conflicts("veclibfort")

    conflicts("gcc@:6")  # support for OpenMP 4+ is required, available in 7.0

    # only GCC 7 and higher have sufficient support for OpenMP tasks
    conflicts("%gcc@3.0:6.999")
    conflicts("%cce")
    conflicts("%clang")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    patch("remove_absolute_mkl_include.patch", when="@17.1")

    def edit(self, spec, prefix):
        # copy "make.inc.mkl-gcc" provided by default into "make.inc"
        open("make.inc", "w").write(open("make.inc.mkl-gcc").read())

        make_inc = FileFilter("make.inc")
        make_inc.filter("-DPLASMA_WITH_MKL", "")  # not using MKL
        # pass prefix variable from "make.inc" to "Makefile"
        make_inc.filter("# --*", "prefix={0}".format(self.prefix))

        makefile = FileFilter("Makefile")
        makefile.filter("CC *[?]*= * cc", "")

    @property
    def build_targets(self):
        targets = list()

        # use $CC set by Spack
        targets.append("CC = {0}".format(env["CC"]))

        # pass BLAS library flags
        targets.append("LIBS = {0}".format(self.spec["blas"].libs.ld_flags))

        return targets
