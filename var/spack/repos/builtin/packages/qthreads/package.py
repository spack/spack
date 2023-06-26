# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def is_integer(x):
    """Any integer value"""

    try:
        return float(x).is_integer()
    except ValueError:
        return False


class Qthreads(AutotoolsPackage):
    """The qthreads API is designed to make using large numbers of
    threads convenient and easy, and to allow portable access to
    threading constructs used in massively parallel shared memory
    environments. The API maps well to both MTA-style threading and
    PIM-style threading, and we provide an implementation of this
    interface in both a standard SMP context as well as the SST
    context. The qthreads API provides access to full/empty-bit
    (FEB) semantics, where every word of memory can be marked
    either full or empty, and a thread can wait for any word to
    attain either state."""

    homepage = "http://www.cs.sandia.gov/qthreads/"

    test_requires_compiler = True
    test_base_path = "test/basics/"
    test_list = ["hello_world_multi", "hello_world"]

    tags = ["e4s"]

    version("1.18", sha256="d1a808b35d3af0012194a8f3afe72241dfcffca7e88a7104fa02a46c73022880")
    version("1.17", sha256="b17efb3c94c2027b8edd759584f4b1fa1e2725f1878a7a098d7bc58ad38d82f1")
    version("1.16", sha256="923d58f3ecf7d838a18c3616948ea32ddace7196c6805518d052c51a27219970")
    version("1.15", sha256="3ac2dc24debff004a2998933de5724b1e14e1ae262fa9942acbb01f77819a23b")
    version("1.14", sha256="16f15e5b2e35b6329a857d24c283a1e43cd49921ee49a1446d4f31bf9c6f5cf9")
    version("1.12", sha256="2c13a5f6f45bc2f22038d272be2e748e027649d3343a9f824da9e86a88b594c9")
    version("1.11", sha256="dbde6c7cb7de7e89921e47363d09cecaebf775c9d090496c2be8350355055571")
    version("1.10", sha256="29fbc2e54bcbc814c1be13049790ee98c505f22f22ccee34b7c29a4295475656")

    patch("restrict.patch", when="@:1.10")
    patch("trap.patch", when="@:1.10")

    variant("hwloc", default=True, description="hwloc support")
    variant("spawn_cache", default=False, description="enables worker specific cache of spawns")
    variant(
        "scheduler",
        default="nemesis",
        values=("nemesis", "lifo", "mutexfifo", "mtsfifo", "sherwood", "distrib", "nottingham"),
        multi=False,
        description="Specify which scheduler policy to use",
    )
    variant("static", default=True, description="Build static library")
    variant(
        "stack_size",
        default=4096,
        description="Specify number of bytes to use in a stack",
        values=is_integer,
    )

    depends_on("hwloc@1.0:1", when="@:1.15 +hwloc")
    depends_on("hwloc@1.5:2", when="@1.16: +hwloc")

    def url_for_version(self, version):
        # if version is greater than 1.17, use new default
        if version >= Version("1.17"):
            url_fmt = (
                "https://github.com/Qthreads/qthreads/releases/download/{0}/qthread-{0}.tar.gz"
            )
        # otherwise, use .bz2 file format
        else:
            url_fmt = (
                "https://github.com/Qthreads/qthreads/releases/download/{0}/qthread-{0}.tar.bz2"
            )
        return url_fmt.format(version)

    def configure_args(self):
        spec = self.spec
        if "+hwloc" in self.spec:
            args = [
                "--enable-guard-pages",
                "--with-topology=hwloc",
                "--with-hwloc=%s" % spec["hwloc"].prefix,
            ]
        else:
            args = ["--with-topology=no"]

        if "+spawn_cache" in self.spec:
            args.append("--enable-spawn-cache")
        else:
            args.append("--disable-spawn-cache")

        if "+static" in self.spec:
            args.append("--enable-static=yes")
        else:
            args.append("--enable-static=no")

        args.append("--with-default-stack-size=%s" % self.spec.variants["stack_size"].value)

        args.append("--with-scheduler=%s" % self.spec.variants["scheduler"].value)
        return args

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        tests = self.test_list
        relative_test_dir = self.test_base_path
        files_to_cpy = []
        header = "test/argparsing.h"
        for test in tests:
            test_path = join_path(relative_test_dir, test + ".c")
            files_to_cpy.append(test_path)
        files_to_cpy.append(header)
        self.cache_extra_test_sources(files_to_cpy)

    def build_tests(self):
        """Build and run the added smoke (install) test."""
        tests = self.test_list
        relative_test_dir = self.test_base_path

        for test in tests:
            options = [
                "-I{0}".format(self.prefix.include),
                "-I{0}".format(self.install_test_root + "/test"),
                join_path(self.install_test_root, relative_test_dir, test + ".c"),
                "-o",
                test,
                "-L{0}".format(self.prefix.lib),
                "-lqthread",
                "{0}{1}".format(self.compiler.cc_rpath_arg, self.prefix.lib),
            ]
            reason = "test:{0}: Checking ability to link to the library.".format(test)
            self.run_test("cc", options, [], installed=False, purpose=reason)

    def run_tests(self):
        tests = self.test_list
        # Now run the program
        for test in tests:
            reason = "test:{0}: Checking ability to execute.".format(test)
            self.run_test(test, [], purpose=reason)

    def test(self):
        # Build
        self.build_tests()
        # Run test programs pulled from the build
        self.run_tests()
