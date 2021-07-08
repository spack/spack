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
#     spack install py-sphobjinv
#
# You can edit this file again by typing:
#
#     spack edit py-sphobjinv
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PySphobjinv(PythonPackage):
    """Sphinx objects.inv Inspection/Manipulation Tool."""

    homepage = "https://github.com/bskinn/sphobjinv"
    url      = "https://github.com/bskinn/sphobjinv/archive/refs/tags/v2.1.tar.gz"

    version('2.1', sha256='e41950a578dfd5acae24f12c7fe12b8d5e44f9162487aaa27189ca2e5c45d30c')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-attrs@19.2:', type=('build', 'run'))
    depends_on('py-certifi', type=('build', 'run'))
    depends_on('py-fuzzywuzzy@0.8:', type=('build', 'run'))
    depends_on('py-jsonschema@3.0:', type=('build', 'run'))
