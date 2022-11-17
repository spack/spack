# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *

# OmpSs-2 is a complex package to build as it has multiple parts that need to be built separately
# Moreover, some of these parts use Autotools and then the LLVM compiler uses CMake


class Ompss2(Package):
    """OmpSs-2 is a data-flow shared-memory programming model based on source annotations.
    It is developed by the Barcelona Supercomputing Center as a successor to the StarSs and
    OmpSs programming models."""

    homepage = "https://pm.bsc.es/ompss-2"

    maintainers = ["dave96"]

    version("2021.11.1", sha256="9e0ee0c9f75cd558882465efc3d521c2fe93f1a6b50d4d9c8e614ab4eb3a9e6c")

    depends_on("extrae")
    depends_on("hwloc")
    depends_on("sqlite")
    depends_on("python", type="build")
    depends_on("cmake", type="build")

    resource(
        name="jemalloc",
        url="https://github.com/jemalloc/jemalloc/releases/download/5.3.0/jemalloc-5.3.0.tar.bz2",
        sha256="2db82d1e7119df3e71b7640219b6dfe84789bc0537983c3b7ac4f7189aecfeaa",
        destination="jemalloc",
    )

    parallel = True

    # Patch mercurium to tolerate the libiconv that is inserted by spack into the build environment
    def patch(self):
        os.chdir(glob.glob("./mcxx-*").pop())

        filter_file(r"AM_LDFLAGS=", "AM_LDFLAGS=$(LIBICONV)", "Makefile.am")

        os.chdir("..")

    # Special URL handling since the -2 suffix messes with spacks default url scheme
    def url_for_version(self, version):
        url = "https://pm.bsc.es/ftp/ompss-2/releases/ompss-2-{0}.tar.gz"
        return url.format(version)

    def install_jemalloc(self, spec, prefix):
        os.chdir("./jemalloc/jemalloc-5.3.0")

        configure("--prefix=%s" % prefix, "--with-jemalloc-prefix=nanos6_je_")

        make()
        make("install")

        os.chdir("../..")

    def install_mcxx(self, spec, prefix):
        os.chdir(glob.glob("./mcxx-*").pop())

        reconf = which("autoreconf")
        reconf("-fiv")

        configure(
            "--prefix=%s" % prefix,
            "--with-nanos6=%s" % prefix,
            "--enable-ompss-2",
        )
        make()
        make("install")
        os.chdir("..")

    def install_llvm(self, spec, prefix):
        os.chdir(glob.glob("./llvm*").pop())
        mkdirp("./build")
        os.chdir("./build")

        cmake = which("cmake")
        cmake(
            "../llvm",
            "-G Unix Makefiles",
            "-DCMAKE_INSTALL_PREFIX=%s" % prefix,
            "-DCMAKE_BUILD_TYPE=Release",
            "-DLLVM_PARALLEL_LINK_JOBS=1",
            "-DCLANG_DEFAULT_NANOS6_HOME=%s" % prefix,
            "-DLLVM_ENABLE_PROJECTS=clang",
            "-DCLANG_DEFAULT_PIE_ON_LINUX=OFF",
            "-DLLVM_INSTALL_UTILS=ON",
            "-DLLVM_INCLUDE_BENCHMARKS=OFF",
        )
        make()
        make("install")

        os.chdir("../..")

    def install_nanos6(self, spec, prefix):
        os.chdir(glob.glob("./nanos6-*").pop())
        configure(
            "--prefix=%s" % prefix,
            "--with-jemalloc=%s" % prefix,
            "--with-extrae=%s" % spec["extrae"].prefix,
            "--with-hwloc=%s" % spec["hwloc"].prefix,
            "--disable-stats-instrumentation",
            "--disable-verbose-instrumentation",
            "--disable-lint-instrumentation",
            "--disable-graph-instrumentation",
            "--without-papi",
        )

        make()
        make("install")
        os.chdir("..")

    def install(self, spec, prefix):
        self.install_jemalloc(spec, prefix)
        self.install_nanos6(spec, prefix)
        self.install_mcxx(spec, prefix)
        self.install_llvm(spec, prefix)
