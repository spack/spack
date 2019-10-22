# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nccmp(Package):
    """Compare NetCDF Files"""
    homepage = "http://nccmp.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/nccmp/nccmp-1.8.2.0.tar.gz"

    version('1.8.2.0', sha256='7f5dad4e8670568a71f79d2bcebb08d95b875506d3d5faefafe1a8b3afa14f18')

    depends_on('netcdf')

    def install(self, spec, prefix):
        # Configure says: F90 and F90FLAGS are replaced by FC and
        # FCFLAGS respectively in this configure, please unset
        # F90/F90FLAGS and set FC/FCFLAGS instead and rerun configure
        # again.
        env.pop('F90', None)
        env.pop('F90FLAGS', None)

        configure('--prefix=%s' % prefix)
        make()
        make("check")
        make("install")
