# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('3.450', sha256='bf6012dbe668ecb22c399c4b7b2814557ee282c74a7d5dc704eb17c30d9fb92e')
    version('3.420', sha256='6c10aa636118fa12d9a5e2e66f22c6436fb358da2af6dbf7e133c142e2ac16b8')
    version('3.410', sha256='a556ac7ea1965545dcb4d41cfef8e4915eeb8c0faa1b52f7ff70870f8bb5734c')
    version('3.370', sha256='092897c6dae4dfe42d91d35a738e45e8236aa3d8f9b3ffc7f0e6545b8319c63a')

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
