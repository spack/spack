# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PySvgpathtools(PythonPackage):
    """A collection of tools for manipulating and analyzing SVG Path objects
    and Bezier curves."""

    homepage = "https://pypi.org/project/svgpathtools/"
    url      = "https://pypi.io/packages/source/s/svgpathtools/svgpathtools-1.3.3.tar.gz"

    version('1.3.3', '253714213424e73b67a73c1fd73b714e')

    depends_on('py-setuptools', type='build')
