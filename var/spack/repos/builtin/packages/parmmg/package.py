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
#     spack install parmmg
#
# You can edit this file again by typing:
#
#     spack edit parmmg
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Parmmg(CMakePackage):
    """ParMMG is a parallel remesher based on MMG"""

    homepage = "https://www.mmgtools.org"
    url      = "https://github.com/MmgTools/ParMmg/archive/refs/tags/v1.3.0.tar.gz"

    maintainers = ['corentin-dev']

    version('1.3.0', sha256='d43b73a73b62545b5a31bbe25562f69c9e63ad8a6d416bd459781203e37427cf')
    version('1.2.0', sha256='99729cc292dcb59c87e3f25d4cabf5a64841e83b624d383e1fd3fb7f960df672')
    version('1.1.0', sha256='a5904f1f56b7809ab9ec2f6118b03a082ec2b5564355a73c74fc55426cc69600')
    version('1.0.0', sha256='614feb815ff6cdfc9bced30e8105994f0bf3a812243619d3349203ec1851cf6d')

    depends_on('mmg')
    depends_on('metis')
    depends_on('vtk')
    depends_on('mpi')

    def cmake_args(self):
        args = []
        return args
