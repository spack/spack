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
#     spack install professor
#
# You can edit this file again by typing:
#
#     spack edit professor
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Professor(Package):
    """Install package for the Professor tuning software."""

    homepage = "https://professor.hepforge.org/"
    url      = "https://professor.hepforge.org/downloads/?f=Professor-2.3.3.tar.gz"

    # notify when the package is updated.
    maintainers = ['mjk655']

    version('2.3.3', sha256='60c5ba00894c809e2c31018bccf22935a9e1f51c0184468efbdd5d27b211009f')

    # FIXME: Add dependencies if required.
    depends_on('eigen')
    depends_on('py-cython')
    depends_on('py-iminuit')
    depends_on('py-matplotlib')
    

    def install(self, spec, prefix):
        #makefile = FileFilter('Makefile')
        #makefile.filter('CC = .*', 'CC = cc')
        make()
        make("install")
        
