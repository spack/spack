# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyzmq(PythonPackage):
    """Python bindings for 0MQ"""

    homepage = "https://pyzmq.readthedocs.org"
    pypi = "pyzmq/pyzmq-24.0.1.tar.gz"

    version("24.0.1", sha256="216f5d7dbb67166759e59b0479bca82b8acf9bed6015b526b8eb10143fb08e77")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="build")
