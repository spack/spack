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
#     spack install spm
#
# You can edit this file again by typing:
#
#     spack edit spm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Spm(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/spm12_r7219.zip"

    version('12_r7219', sha256='b46fe8ce5ab537caeea7634c650f3a12fe2716f6a2e8ac15aa0d62b3652fe764')

    depends_on('zip', type='build')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        unzip = which('unzip')
        unzip('spm12.ctf')

        bash = which('bash')
        bash('./run_spm12.sh')

        install_tree('spm12', prefix)
