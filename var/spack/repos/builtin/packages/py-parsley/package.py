# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyParsley(PythonPackage):
    """Parsing and pattern matching made easy."""

    homepage = "https://launchpad.net/parsley"
    pypi = "Parsley/Parsley-1.3.tar.gz"

    license("MIT")

    version(
        "1.3",
        sha256="c3bc417b8c7e3a96c87c0f2f751bfd784ed5156ffccebe2f84330df5685f8dc3",
        url="https://pypi.org/packages/2b/d6/4fed8d65e28a970e1c5cb33ce9c7e22e3de745e1b2ae37af051ef16aea3b/Parsley-1.3-py2.py3-none-any.whl",
    )
