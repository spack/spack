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
#     spack install hoppet
#
# You can edit this file again by typing:
#
#     spack edit hoppet
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Hoppet(AutotoolsPackage):
    """A Fortran 95 package for carrying out QCD DGLAP evolution and other common manipulations of parton distribution functions (PDFs)."""

    homepage = "https://hoppet.hepforge.org/"
    url      = "https://github.com/gavinsalam/hoppet/archive/refs/tags/hoppet-1.2.0.tar.gz"


    # maintainers = ['haralmha']

    version('1.2.0', sha256='6e00eb56a4f922d03dfceba7b389a3aaf51f277afa46d7b634d661e0797e8898')
    

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
