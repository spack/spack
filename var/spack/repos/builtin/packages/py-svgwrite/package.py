# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PySvgwrite(PythonPackage):
    """A Python library to create SVG drawings."""

    homepage = "https://pypi.org/project/svgwrite/"
    url      = "https://pypi.io/packages/source/s/svgwrite/svgwrite-1.1.12.zip"

    version('1.1.12', '05780a4a8ba33c16842faf37818d670e')

    depends_on('py-setuptools', type='build')
