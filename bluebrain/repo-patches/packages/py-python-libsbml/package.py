# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install py-libsbml
#
# You can edit this file again by typing:
#
#     spack edit py-libsbml
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPythonLibsbml(PythonPackage):
    """LibSBML is a library for reading, writing and manipulating the Systems Biology
    Markup Language (SBML)."""

    homepage = "https://sbml.org/"
    url      = "https://github.com/sbmlteam/python-libsbml"
    git      = "https://github.com/sbmlteam/python-libsbml.git"

    version('5.19.5', tag='v5.19.5', submodules=True)

    depends_on('py-setuptools', type='build')

    depends_on('swig@2:', type='build')
    depends_on('cmake', type='build')
    depends_on('zlib')
    depends_on('bzip2')
    depends_on('libxml2')
