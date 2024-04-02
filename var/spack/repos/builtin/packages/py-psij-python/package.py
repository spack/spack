# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsijPython(PythonPackage):
    """PSI/J is an abstraction layer over cluster schedulers to write scheduler
    agnostic HPC applications."""

    homepage = "https://www.exaworks.org/"
    git = "https://github.com/exaworks/psij-python.git"
    pypi = "psij-python/psij-python-0.1.0.post2.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version(
        "0.1.0.post2",
        sha256="427c58dda028e6dec222bc45ebaec13d843a28696cc96814355ca6efe4d739b1",
        url="https://pypi.org/packages/8c/38/ba44be75f86d32df45d2deb275c9c250bf71a2629fd6ca4ee1def5739d25/psij_python-0.1.0.post2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-filelock", when="@:0.1")
        depends_on("py-psutil", when="@:0.1")
        depends_on("py-pystache@0.6:")
