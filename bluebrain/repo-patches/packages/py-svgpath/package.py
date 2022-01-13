# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PySvgpath(PythonPackage):
    """svg.path is a collection of objects that implement the different path
    commands in SVG, and a parser for SVG path definitions.
    """

    homepage = "https://github.com/regebro/svg.path"
    url      = "https://pypi.io/packages/source/s/svg.path/svg.path-4.1.tar.gz"
    git      = "https://github.com/regebro/svg.path.git"

    version('4.1', sha256='7e6847ba690ff620e20f152818d52e1685b993aacbc41b321f8fee3d1cb427db')
    depends_on('py-setuptools', type='build')
