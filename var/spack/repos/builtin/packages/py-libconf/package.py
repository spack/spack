# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibconf(PythonPackage):
    """A pure-Python libconfig reader/writer with permissive license"""

    pypi = "libconf/libconf-2.0.1.tar.gz"

    license("MIT")

    version(
        "2.0.1",
        sha256="b9e9bc79d0e22a9c6239a16cd8ecf198114395c4365b9fb62c39cffff0593ffc",
        url="https://pypi.org/packages/0b/c1/f3345223779616ef4df444a5721123cc84bf45b5b56d6f6efba62bf83383/libconf-2.0.1-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="06a7107729bce8df985cd98f5ca5c65e3238893252e9ae3c2aae6b7b71fc8c83",
        url="https://pypi.org/packages/bf/2a/eebafba3819655fcfd03ce1fdee53726139eb30339b2db7ade29a75eb01f/libconf-1.0.1-py2.py3-none-any.whl",
    )
