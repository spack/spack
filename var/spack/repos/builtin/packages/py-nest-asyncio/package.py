# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNestAsyncio(PythonPackage):
    """Patch asyncio to allow nested event loops."""

    homepage = "https://github.com/erdewit/nest_asyncio"
    pypi = "nest-asyncio/nest_asyncio-1.4.0.tar.gz"

    version("1.5.5", sha256="e442291cd942698be619823a17a86a5759eabe1f8613084790de189fe9e16d65")
    version("1.5.4", sha256="f969f6013a16fadb4adcf09d11a68a4f617c6049d7af7ac2c676110169a63abd")
    version("1.5.1", sha256="afc5a1c515210a23c461932765691ad39e8eba6551c055ac8d5546e69250d0aa")
    version("1.4.0", sha256="5773054bbc14579b000236f85bc01ecced7ffd045ec8ca4a9809371ec65a59c8")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4.3: +toml", type="build")
