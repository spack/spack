# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyObjectstore(PythonPackage):
    """The Galaxy object store framework and default implementations."""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-objectstore/galaxy-objectstore-22.1.1.tar.gz"

    license("CC-BY-3.0")

    version(
        "22.1.1",
        sha256="57a9c4d1390cb497409c5a3d045b8dc47f08cb66d35b36c4c98b27f33999049c",
        url="https://pypi.org/packages/b0/0b/6ba4e0b8e1baab4f0f369014b9a5c16c488ce6b89dba22fd4f9897d86fbf/galaxy_objectstore-22.1.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-galaxy-util")
        depends_on("py-pyyaml", when="@20:")
