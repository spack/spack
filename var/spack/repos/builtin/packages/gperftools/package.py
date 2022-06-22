# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gperftools(CMakePackage):
    """Google's fast malloc/free implementation, especially for
       multi-threaded applications.  Contains tcmalloc, heap-checker,
       heap-profiler, and cpu-profiler.

    """
    homepage = "https://github.com/gperftools/gperftools"
    url = "https://github.com/gperftools/gperftools/archive/refs/tags/gperftools-0.0.tar.gz"
    maintainers = ["albestro", "eschnett", "msimberg", "teonnik"]

    version('2.10', sha256='83e3bfdd28b8bcf53222c3798d4d395d52dadbbae59e8730c4a6d31a9c3732d8')
    version('2.9.1', sha256='484a88279d2fa5753d7e9dea5f86954b64975f20e796a6ffaf2f3426a674a06a')
    version('2.8.1', sha256='260c510b742e44bc53465a1e9b3294f290525360658a6d1612019df2c2f7f307')
    version('2.7', sha256='1ee8c8699a0eff6b6a203e59b43330536b22bbcbe6448f54c7091e5efb0763c9', deprecated=True)
    version('2.4', sha256='982a37226eb42f40714e26b8076815d5ea677a422fb52ff8bfca3704d9c30a2d', deprecated=True)
    version('2.3', sha256='093452ad45d639093c144b4ec732a3417e8ee1f3744f2b0f8d45c996223385ce', deprecated=True)

    variant("sized_delete", default=False, description="Build sized delete operator")
    variant("dynamic_sized_delete_support", default=False, description="Try to build run-time switch for sized delete operator")
    variant("debugalloc", default=True, description="Build versions of libs with debugalloc")
    variant("libunwind", default=True, description="Enable libunwind linking")

    depends_on("unwind", when="+libunwind")

    def cmake_args(self):
        args = [
            self.define_from_variant("gperftools_sized_delete", "sized_delete"),
            self.define_from_variant("gperftools_dynamic_sized_delete_support", "dynamic_sized_delete_support"),
            self.define_from_variant("GPERFTOOLS_BUILD_DEBUGALLOC", "debugalloc"),
            self.define_from_variant("gperftools_enable_libunwind", "libunwind"),
        ]
        return args

    # All of the below can be removed when the deprecated Autotools-based
    # versions are removed (2.7 and older)
    def url_for_version(self, version):
        if self.spec.satisfies("@2.8:"):
            return "https://github.com/gperftools/gperftools/archive/refs/tags/gperftools-{}.tar.gz".format(version)
        else:
            return "https://github.com/gperftools/gperftools/releases/download/gperftools-{}/gperftools-{}.tar.gz".format(version, version)

    def configure_args(self):
        def enable_or_disable(option, variant):
            if variant not in self.variants:
                raise KeyError("Invalid variant {} given for gperftools".format(variant))
            if self.spec.variants[variant].value:
                return "--enable-" + option
            else:
                return "--disable-" + option

        args = [
            enable_or_disable("sized-delete", "sized_delete"),
            enable_or_disable("dynamic-sized-delete-support", "dynamic_sized_delete_support"),
            enable_or_disable("debugalloc", "debugalloc"),
            enable_or_disable("libunwind", "debugalloc"),
        ]
        if self.spec.satisfies('+libunwind'):
            args += [
                "LDFLAGS=-lunwind"
            ]
        return args

    @property
    def build_directory(self):
        if self.spec.satisfies("@:2.7"):
            return self.stage.source_path
        else:
            return os.path.join(self.stage.path, self.build_dirname)

    @when("@:2.7")
    def cmake(self, spec, prefix):
        configure("--prefix={0}".format(self.prefix), *self.configure_args())
