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
    version("17.1",
        sha256="d4b89f7c3d240a69dfe986284a14471eec4830b9e352ae902ea8861f15573dee",
        url="https://bitbucket.org/icl/plasma/downloads/plasma-17.1.tar.gz")

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

    patch("remove_absolute_mkl_include.patch", when="@17.1")

    @when("@18.9.0:")
    def cmake_args(self):
        if self.spec.satisfies('@:17.1'):
            open("CMakeLists.txt", "w").write("cmake_minimum_required( VERSION 3.0 FATAL_ERROR )\n")

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

    # Before 18.9.0 it was an Makefile package
    @when("@:17.1")
    def cmake(self, spec, prefix):
        pass

    # Before 18.9.0 it was an Makefile package
    @when("@:17.1")
    def build(self, spec, prefix):
        pass

    # Before 18.9.0 it was an Makefile package
    @when("@:17.1")
    def install(self, spec, prefix):
        self.edit(spec, prefix)
        make()
        make("install")

    @when("@:17.1")
    def edit(self, spec, prefix):
        # copy "make.inc.mkl-gcc" provided by default into "make.inc"
        open("make.inc", "w").write(open("make.inc.mkl-gcc").read())

        make_inc = FileFilter("make.inc")

        if not spec.satisfies("^intel-mkl"): # or not env.has_key("MKLROOT"):
            make_inc.filter("-DPLASMA_WITH_MKL", "")  # not using MKL
            make_inc.filter("LIBS *= *.*", "LIBS = " +
                self.spec["blas"].libs.ld_flags + " -lm")

        header_flags = ""
        # accumulate CPP flags for headers: <cblas.h> and <lapacke.h>
        for dep in ("blas", "lapack"):
            try:  # in case the dependency does not provide header flags
                header_flags += " " + spec[dep].headers.cpp_flags
            except AttributeError:
                pass

        make_inc.filter("CFLAGS +[+]=", "CFLAGS += " + header_flags + " ")

        # pass prefix variable from "make.inc" to "Makefile"
        make_inc.filter("# --*", "prefix={0}".format(self.prefix))

        # make sure CC variable comes from build environment
        make_inc.filter("CC *[?]*= * .*cc", "")

    @property
    def build_targets(self):
        targets = list()

        if self.spec.satisfies('@18.9.0:'):
            return targets

        # use $CC set by Spack
        targets.append("CC = {0}".format(self.compiler.cc))

        if self.spec.satisfies("^intel-mkl"):
            targets.append("MKLROOT = {0}/mkl".format(env["MKLROOT"]))

        # pass BLAS library flags
        targets.append("LIBS = {0}".format(self.spec["blas"].libs.ld_flags))

        return targets
