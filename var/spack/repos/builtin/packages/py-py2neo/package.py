# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy2neo(PythonPackage):
    """Py2neo is a client library and toolkit for working with Neo4j from
    within Python applications and from the command line."""

    homepage = "http://py2neo.org/"
    url      = "https://github.com/nigelsmall/py2neo/archive/py2neo-2.0.8.tar.gz"

    version('2.0.8', sha256='57b4a1c4aa800e03904b2adfd7c8ec467b072bae2d24baf150fd580916255f2e')
    version('2.0.7', sha256='aa7c86fec70823111d2f932cb20a978889f1c47c2f58461309f644ecb9a22204')
    version('2.0.6', sha256='bcf00ebc82a80c7e2da00288e8f90f81682abfc991e19d92d21726c2deac823f')
    version('2.0.5', sha256='024b42261b06e5e2c92a1f24e62398847f090862005add0b5c69a79a7e1e87b5')
    version('2.0.4', sha256='19074b7b892f2e989f39eae21fc59b26a05e1a820adad8aa58bc470b70d9056d')

    depends_on("py-setuptools", type='build')
