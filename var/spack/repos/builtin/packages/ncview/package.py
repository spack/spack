# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ncview(AutotoolsPackage):
    """Simple viewer for NetCDF files."""
    homepage = "http://meteora.ucsd.edu/~pierce/ncview_home_page.html"
    url      = "ftp://cirrus.ucsd.edu/pub/ncview/ncview-2.1.7.tar.gz"

    version('2.1.7', 'debd6ca61410aac3514e53122ab2ba07')

    depends_on('netcdf')
    depends_on('udunits2')
    depends_on('libpng')
    depends_on('libxaw')

    def configure_args(self):
        spec = self.spec

        config_args = []

        if spec.satisfies('^netcdf+mpi'):
            config_args.append('CC={0}'.format(spec['mpi'].mpicc))

        return config_args
