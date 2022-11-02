# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPykml(PythonPackage):
    """pyKML is a Python package for parsing and authoring KML documents.
    It is based on the lxml.objectify API which provides Pythonic access to
    XML documents.
    """

    pypi = "pykml/pykml-0.1.3.tar.gz"

    version("0.2.0", sha256="44a1892e7c2a649c8ae9f8e2899ff76cae79ec6749ffb64d11140b4e87d0f957")
    version("0.1.3", sha256="e1a133e582f0b4652a6b00bac970b446d90580664e5a634a670731c990ff9f05")

    depends_on("python@2", type=('build', 'run'), when='@0.1')
    depends_on("py-setuptools", type="build")
    depends_on("py-lxml@3.3.6:", type=("build", "run"), when='@0.2.0:')
    depends_on("py-lxml@2.2.6:", type=("build", "run"))
