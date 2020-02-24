# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Hcol(Package):
    """This is the SPIRAL package for the Hybrid Control Operator Language (HCOL)."""

    homepage = "https://https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-hcol/archive/1.0.0.zip"

    maintainers = ['spiralgen']
    extends('spiral')

    version('1.0.0', sha256='9a95574e2b061d03d264c32dbf733e893017d1644b6486c7a8a55a3b24783f58')

    # HCOL package is a set of files to be installed in the
    # "namespaces/packages" folder (subfolder hcol for this package).  No other
    # operations are required to build" 
    def install(self, spec, prefix):
        source = self.stage.source_path
        print('install method: source = ' + source)
        dest = spec['spiral'].prefix
        print('spiral prefix = ' + dest)
        mkdirp(dest.namespaces.packages.hcol)
        install_tree(source, dest.namespaces.packages.hcol)

