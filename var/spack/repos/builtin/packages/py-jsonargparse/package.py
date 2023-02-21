# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonargparse(PythonPackage):
    """An extension to python's argparse which simplifies parsing of configuration options from
    command line arguments, json configuration files (yaml or jsonnet supersets), environment
    variables and hard-coded defaults.
    """

    homepage = "https://github.com/omni-us/jsonargparse"
    pypi = "jsonargparse/jsonargparse-4.19.0.tar.gz"

    version("4.19.0", sha256="63aa3c7bbdb219d0f254a5ae86f3d54384ebc1ffa905e776cc19283bc843787b")

    variant("signatures", default=False, description="Enable signature features")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@3.13:", type=("build", "run"))

    with when("+signatures"):
        depends_on("py-docstring-parser@0.15:", type=("build", "run"))
        depends_on("py-typeshed-client@2.1:", type=("build", "run"))
