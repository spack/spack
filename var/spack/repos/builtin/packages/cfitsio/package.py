# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cfitsio(AutotoolsPackage):
    """CFITSIO is a library of C and Fortran subroutines for reading and writing
    data files in FITS (Flexible Image Transport System) data format.
    """

    homepage = 'http://heasarc.gsfc.nasa.gov/fitsio/'
    url      = 'http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio3450.tar.gz'

    version('3.450', 'f470849bb43561d9a9b1925eeb7f7f0d')
    version('3.420', '26e5c0dfb85b8d00f536e706305caa13')
    version('3.410', '8a4a66fcdd816aae41768baa0b025552')
    version('3.370', 'abebd2d02ba5b0503c633581e3bfa116')

    variant('bzip2', default=True, description='Enable bzip2 support')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('curl')
    depends_on('bzip2', when='+bzip2')

    def url_for_version(self, version):
        url = 'http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio{0}.tar.gz'
        return url.format(version.joined)

    def configure_args(self):
        spec = self.spec
        extra_args = []
        if '+bzip2' in spec:
            extra_args.append('--with-bzip2=%s' % spec['bzip2'].prefix),
        return extra_args

    @property
    def build_targets(self):
        targets = ['all']

        # Build shared if variant is set.
        if '+shared' in self.spec:
            targets += ['shared']

        return targets
