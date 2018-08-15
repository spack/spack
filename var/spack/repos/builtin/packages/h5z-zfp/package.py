##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class H5zZfp(MakefilePackage):
    """A highly flexible floating point and integer compression plugin for the
       HDF5 library using ZFP compression."""

    homepage = "http://h5z-zfp.readthedocs.io/en/latest"
    git      = "https://github.com/LLNL/H5Z-ZFP.git"

    version('develop', tag='master')
    version('0.8.0', commit='af165c4')
    version('0.7.0', commit='58ac811')

    variant('fortran', default=True, description='Enable Fortran support')

    depends_on('hdf5+fortran', when='+fortran')
    depends_on('hdf5',         when='~fortran')
    depends_on('zfp bsws=8')

    @property
    def make_defs(self):
        make_defs = [
            'PREFIX=%s' % prefix,
            'CC=%s' % spack_cc,
            'HDF5_HOME=%s' % self.spec['hdf5'].prefix,
            'ZFP_HOME=%s' % self.spec['zfp'].prefix]

        if '+fortran' in self.spec and spack_fc:
            make_defs += ['FC=%s' % spack_fc]

        return make_defs

    @property
    def build_targets(self):
        targets = ['all']
        return self.make_defs + targets

    @property
    def install_targets(self):
        make_args = ['install']
        return make_args + self.make_defs
