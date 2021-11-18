# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
#
# To install trexio package in the current envionment
#
#     spack install trexio
#
# You can edit this file again by typing:
#
#     spack edit trexio
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Trexio(AutotoolsPackage):
    """TREXIO: TREX I/O library."""

    homepage = "https://trex-coe.github.io/trexio"
    git      = "https://github.com/TREX-CoE/trexio/"
    url      = "https://github.com/TREX-CoE/trexio/releases/download/v2.0/trexio-2.0.0.tar.gz"

    # notify when the package is updated.
    maintainers = ['q-posev', 'scemama']

    version('master', branch='master')
    version('2.0.0', sha256='6eeef2da44259718b43991eedae4b20d4f90044e38f3b44a8beea52c38b14cb4')

    variant('hdf5', default=True, description='Enable HDF5 support')

    depends_on('emacs@26.0:', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    depends_on("m4", type='build')
    depends_on("hdf5@1.8:+hl", when='+hdf5')

    # This patch is needed to append -lhdf5_hl to $LIBS because by default
    # ./configure cannot properly compile the hdf5_hl test (AC_HAVE_LIBRARY) and thus does not link it.
    def configure_args(self):
        cflags = []
        cppflags = []
        ldflags = []
        libs = []

        hdf5_hl = self.spec['hdf5:hl']
        #ldflags.append(hdf5_hl.libs.search_flags)
        #libs.append(hdf5_hl.libs.link_flags)
        libs.append('-lhdf5_hl')
 
        config_args = []

        config_args.append('CFLAGS=' + ' '.join(cflags))
        config_args.append('CPPFLAGS=' + ' '.join(cppflags))
        config_args.append('LDFLAGS=' + ' '.join(ldflags))
        config_args.append('LIBS=' + ' '.join(libs))

        return config_args


