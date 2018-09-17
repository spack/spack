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


class Codes(AutotoolsPackage):
    """ CO-Design of multi-layer Exascale Storage (CODES) simulation framework
    """

    homepage = "http://www.mcs.anl.gov/projects/codes"
    git      = "https://xgitlab.cels.anl.gov/codes/codes.git"

    version('develop', branch='master')
    version('1.0.0', tag='1.0.0')

    variant('dumpi', default=False, description="Enable DUMPI support")

    # Build dependencies
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('pkg-config', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')

    depends_on('mpi')
    depends_on('ross')
    depends_on('sst-dumpi', when="+dumpi")

    # add the local m4 directory to the search path
    autoreconf_extra_args = ["-Im4"]
    # Testing if srcdir is '.' in configure.ac does not work with spack
    patch('codes-1.0.0.patch')

    def configure_args(self):
        spec = self.spec

        config_args = [
            "CC=%s" % spec['mpi'].mpicc,
            "CXX=%s" % spec['mpi'].mpicxx,
            "PKG_CONFIG_PATH=%s/pkgconfig" % spec['ross'].prefix.lib]

        if "+dumpi" in spec:
            config_args.extend([
                '--with-dumpi=%s'.format(spec['sst-dumpi'].prefix)])

        return config_args
