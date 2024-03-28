# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCheroot(PythonPackage):
    """Highly-optimized, pure-python HTTP server"""

    homepage = "https://cheroot.readthedocs.io/en/latest/"
    pypi = "cheroot/cheroot-6.5.5.tar.gz"

    license("BSD-3-Clause")

    version(
        "8.3.0",
        sha256="2b48c88959b5b80a79aca627ae5212acb398becaa70b576b8b89bec1ad0d1367",
        url="https://pypi.org/packages/20/b0/4e156a205a624bc929673dfa6bcebe4aa6fa00b080dca4dc7b6b50850277/cheroot-8.3.0-py2.py3-none-any.whl",
    )
    version(
        "6.5.5",
        sha256="1593fa2a42b18744ac485aadf5fec4a29ebfee00ba3937a2269b8ffc94447879",
        url="https://pypi.org/packages/3e/50/840039a5350b54fb8efbc3b26c6e4244c9ca24c49ad84fe1f57b1f79ff7d/cheroot-6.5.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-backports-functools-lru-cache", when="@6.2:6.2.2,6.2.4:6.5")
        depends_on("py-jaraco-functools", when="@7:")
        depends_on("py-more-itertools@2.6:", when="@6:")
        depends_on("py-six@1.11:", when="@5.9.2:9")
