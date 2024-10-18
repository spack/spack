# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os.path import dirname, join

from llnl.util import tty

from spack.compiler import Compiler
from spack.version import Version


class Oneapi(Compiler):
    def setup_custom_environment(self, pkg, env):
        # workaround bug in icpx driver where it requires sycl-post-link is on the PATH
        # It is located in the same directory as the driver. Error message:
        #   clang++: error: unable to execute command:
        #   Executable "sycl-post-link" doesn't exist!
        # also ensures that shared objects and libraries required by the compiler,
        # e.g. libonnx, can be found succesfully
        # due to a fix, this is no longer required for OneAPI versions >= 2024.2
        if self.cxx and pkg.spec.satisfies("%oneapi@:2024.1"):
            env.prepend_path("PATH", dirname(self.cxx))
            env.prepend_path("LD_LIBRARY_PATH", join(dirname(dirname(self.cxx)), "lib"))

        # Edge cases for Intel's oneAPI compilers when using the legacy classic compilers:
        # Always pass flags to disable deprecation warnings, since these warnings can
        # confuse tools that parse the output of compiler commands (e.g. version checks).
        if self.cc and self.cc.endswith("icc") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_CFLAGS", "-diag-disable=10441")
        if self.cxx and self.cxx.endswith("icpc") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_CXXFLAGS", "-diag-disable=10441")
        if self.fc and self.fc.endswith("ifort") and self.real_version >= Version("2021"):
            env.append_flags("SPACK_ALWAYS_FFLAGS", "-diag-disable=10448")

        # 2024 release bumped the libsycl version because of an ABI
        # change, 2024 compilers are required.  You will see this
        # error:
        #
        # /usr/bin/ld: warning: libsycl.so.7, needed by ...., not found
        if pkg.spec.satisfies("%oneapi@:2023"):
            for c in ["dnn"]:
                if pkg.spec.satisfies(f"^intel-oneapi-{c}@2024:"):
                    tty.warn(f"intel-oneapi-{c}@2024 SYCL APIs requires %oneapi@2024:")
