# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class HashTest3(Package):
    """Used to test package hashing"""

    homepage = "http://www.hashtest3.org"
    url = "http://www.hashtest1.org/downloads/hashtest3-1.1.tar.bz2"

    version("1.2", sha256="b" * 64)
    version("1.3", sha256="c" * 64)
    version("1.5", sha256="d" * 64)
    version("1.6", sha256="e" * 64)
    version("1.7", sha256="f" * 64)

    variant("variantx", default=False, description="Test variant X")
    variant("varianty", default=False, description="Test variant Y")

    def setup_dependent_build_environment(self, env, dependent_spec):
        pass

    @when("@:1.4")
    def install(self, spec, prefix):
        print("install 1")
        os.listdir(os.getcwd())

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)

    @when("@1.5:")
    def install(self, spec, prefix):
        os.listdir(os.getcwd())

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)

    for _version_constraint in ["@1.5", "@1.6"]:

        @when(_version_constraint)
        def extra_phase(self, spec, prefix):
            pass
