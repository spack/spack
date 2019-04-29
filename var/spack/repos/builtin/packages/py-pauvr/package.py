# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install py-pauvr
#
# You can edit this file again by typing:
#
#     spack edit py-pauvr
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPauvr(PythonPackage):
    """pauvr: a plotting package designed for nanopore and PacBio long reads"""

    homepage = "https://github.com/conchoecia/pauvre"
    url      = "https://github.com/conchoecia/pauvre/archive/0.1.86.tar.gz"

    version('0.1.86', sha256='aa0b3653e7c12fb50a0907ce088d85b8e1b52c97f40e4d2e6e6b7525a681aa1a')

    depends_on('python@3:',        type=('build', 'run'))
    depends_on('py-matplotlib',    type=('build', 'run'))
    depends_on('py-biopython',     type=('build', 'run'))
    depends_on('py-pandas',        type=('build', 'run'))
    depends_on('py-pillow',        type=('build', 'run'))

