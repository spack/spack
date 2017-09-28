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

import os

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

    # installation of Intel's MKL requires access to /opt which is usually restricted
    #depends_on("intel-mkl")

    #depends_on("atlas") # does not have LAPACKE interface
    #depends_on("netlib-lapack@3:3.999+lapacke+external-blas")
    depends_on("netlib-lapack@3:3.999+lapacke")
    #depends_on("cblas") # clashes with OpenBLAS declarations and has a problem compiling on its own
    depends_on("openblas")

    depends_on("gcc@7:", type="build")

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
        open("make.inc","w").write(open("make.inc.mkl-gcc").read())

        make_inc = FileFilter("make.inc")
        make_inc.filter("CC *= *.*", "CC = {0}".format(env["CC"])) # use $CC set by Spack
        make_inc.filter("^LIBS *=.*", "LIBS = -lopenblas -lm")
        make_inc.filter("# --*", "prefix={0}".format(self.prefix))
        make_inc.filter("-DPLASMA_WITH_MKL", "") # not using MKL
        make_inc.filter("# programs", "# {0} {1}".format(os.system(env["CC"] + " -v"), env["SPACK_PREFIX"])) # show Spack's prefix

        makefile = FileFilter("Makefile")
        makefile.filter("CC *[?]*= * cc", "")
