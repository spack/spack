# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Odgi(CMakePackage):
    """Optimized Dynamic Genome/Graph Implementation: understanding pangenome graphs"""

    homepage = "https://odgi.readthedocs.io/"
    url = "https://github.com/pangenome/odgi/releases/download/v0.8.3/odgi-v0.8.3.tar.gz"

    maintainers("tbhaxor")

    version("0.8.3", sha256="13a63b8ada79851fd8ce5e7638dda1a8b75ef0346a5d93552ee2179256eb81bf")
    version("0.8.2", sha256="39ed618e656ade8eabac3f1e8587dccba9faebaf7edf62e5c6924a4ecfd63617")
    version("0.8.1", sha256="7bd5a563b3dbd9551d2ed88b72912caa4cef15ed0b02a092dde0c2b4ee40a09c")
    version("0.8.0", sha256="e21b782ddb6b9322535a8eebeb95fe6c2c795428f07aaad27169c3948ff6c1e6")
    version("0.7.3", sha256="cb2a9f70eb4c7e80141906ec713b00f644beb48723f07b276be2477f0b1af3c0")
    version("0.7.2", sha256="f1108a284acfb62999e2dcd64e023f0d1d30b09351a0215bc851e3a502e33323")
    version("0.7.1", sha256="c5c1f3bdb9315b74e6fa71612c0b9fe4d27883ac213b7cdad7a75d7d59bab62e")
    version("0.7.0", sha256="c143613843f3298a04403ba71fcb30cf5c942d042a913c4217373d23500dc8b7")
    version("0.6.3", sha256="631f2afd605adfa6b5fe5d7775f49ac62f59f99234c35df8501477ad34a7c6fd")
    version("0.6.2", sha256="88b2114a42b130992c16df288012c8e59c7fd4cc405efdf9364099b2c63b8ca0")

    # lib variants
    variant("libdivsufsort", default=False, description="Build with libdivsufsort")
    variant("sdsl-lite", default=False, description="Build with sdsl-lite")

    # build variants
    variant("static", default=False, description="Enable static linking")

    # dependencies
    depends_on("libdivsufsort", when="+libdivsufsort")
    depends_on("sdsl-lite", when="+sdsl-lite +static")
    depends_on("jemalloc")
    depends_on("python+debug")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_STATIC", "static")]

        return args
