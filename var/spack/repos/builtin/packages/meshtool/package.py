# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install meshtool
#
# You can edit this file again by typing:
#
#     spack edit meshtool
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Meshtool(MakefilePackage):
    """Meshtool - A mesh manipulation utility"""

    homepage = "https://bitbucket.org/aneic/meshtool/"
    git      = "https://bitbucket.org/aneic/meshtool.git"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['MarieHouillon']

    version('master', branch='master')
    # Version to use with opencarp@7.0
    version('oc7.0', commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('meshtool', prefix.bin)

