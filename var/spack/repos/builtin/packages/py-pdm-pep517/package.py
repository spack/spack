# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPdmPep517(PythonPackage):
    """A PEP 517 backend for PDM that supports PEP 621 metadata."""

    homepage = "https://pdm.fming.dev/latest/"
    pypi = "pdm-pep517/pdm-pep517-1.0.4.tar.gz"

    license("MIT")

    version(
        "1.0.4",
        sha256="8fd42caeaa2031a41d86bce6519ad96edaf1dfc99cf0c2b6d310d1ae2089bb39",
        url="https://pypi.org/packages/32/56/1d4b069d8c406ba85ef2992a56f6780de6f8e76fef98af7d291138c4221e/pdm_pep517-1.0.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
