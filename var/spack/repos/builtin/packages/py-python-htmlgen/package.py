# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-python-htmlgen
#
# You can edit this file again by typing:
#
#     spack edit py-python-htmlgen
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PythonHtmlgen(PythonPackage):
    """Library to generate HTML from classes.
    """

    homepage = "https://github.com/srittau/python-htmlgen"
    url      = "https://github.com/srittau/python-htmlgen/archive/v1.2.2.tar.gz"

    version('1.2.2', sha256='9dc60e10511f0fd13014659514c6c333498c21779173deb585cd4964ea667770')

    depends_on('py-setuptools', type='build')
    # dependencies for tests
    depends_on('py-typing', type='build')
    # the following spack dependency to be added later
    # depends_on('py-python-asserts', type='build')
