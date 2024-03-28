# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribProgramoutput(PythonPackage):
    """A Sphinx extension to literally insert the output of arbitrary commands
    into documents, helping you to keep your command examples up to date."""

    homepage = "https://sphinxcontrib-programoutput.readthedocs.org/"
    pypi = "sphinxcontrib-programoutput/sphinxcontrib-programoutput-0.15.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.15",
        sha256="8a15af67546c35404a02e0ad13c0a9ded0d587393fca5fa637a467bfee1222f0",
        url="https://pypi.org/packages/34/22/c14806fa02f3a5dd9ebe21fcbd378555a7f0462689895c3fe4d61b9d1e1c/sphinxcontrib_programoutput-0.15-py2.py3-none-any.whl",
    )
    version(
        "0.10",
        sha256="9d665ece29627d87b7e3b678bbba4007f147de0ee27418c66b6128329b0c49ad",
        url="https://pypi.org/packages/c2/70/addc3e19a10558d378ec59e5c00f7c5605ac4e5b09a4f6ef32b62ae0b53d/sphinxcontrib_programoutput-0.10-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-sphinx@1.7.0:", when="@0.15:")
        depends_on("py-sphinx@1.3.5:", when="@0.10")
