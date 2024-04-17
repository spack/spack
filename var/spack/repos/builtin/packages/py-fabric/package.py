# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFabric(PythonPackage):
    """High level SSH command execution."""

    homepage = "http://fabfile.org/"
    pypi = "fabric/fabric-2.5.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "2.5.0",
        sha256="160331934ea60036604928e792fa8e9f813266b098ef5562aa82b88527740389",
        url="https://pypi.org/packages/d7/cb/47feeb00dae857f0fbd1153a61e902e54ed77ccdc578b371a514a3959a19/fabric-2.5.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-invoke@1.3:1", when="@2.5:2")
        depends_on("py-paramiko@2.4:")
