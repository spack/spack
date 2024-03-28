# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyHjson(PythonPackage):
    """Hjson is an user interface for JSON.
    The Python implementation of Hjson is based on simplejson."""

    homepage = "https://github.com/hjson/hjson-py"
    pypi = "hjson/hjson-3.0.2.tar.gz"

    license("AFL-2.1")

    version(
        "3.1.0",
        sha256="65713cdcf13214fb554eb8b4ef803419733f4f5e551047c9b711098ab7186b89",
        url="https://pypi.org/packages/1f/7f/13cd798d180af4bf4c0ceddeefba2b864a63c71645abc0308b768d67bb81/hjson-3.1.0-py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="5546438bf4e1b52bc964c6a47c4ed10fa5fba8a1b264e22efa893e333baad2db",
        url="https://pypi.org/packages/74/da/f7c0e3407f1f600326ff762373f57971a16b771435736b70ce9c24fbe761/hjson-3.0.2-py3-none-any.whl",
    )
