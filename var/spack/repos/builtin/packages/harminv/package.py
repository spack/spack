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


class Harminv(AutotoolsPackage):
    """Harminv is a free program (and accompanying library) to solve the
    problem of harmonic inversion - given a discrete-time, finite-length
    signal that consists of a sum of finitely-many sinusoids (possibly
    exponentially decaying) in a given bandwidth, it determines the
    frequencies, decay constants, amplitudes, and phases of those sinusoids."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Harminv"
    url      = "http://ab-initio.mit.edu/harminv/harminv-1.4.tar.gz"
    list_url = "http://ab-initio.mit.edu/harminv/old"

    version('1.4', 'b95e24a9bc7e07d3d2202d1605e9e86f')

    depends_on('blas')
    depends_on('lapack')

    def configure_args(self):
        spec = self.spec

        return [
            '--enable-shared',
            '--with-blas={0}'.format(spec['blas'].prefix.lib),
            '--with-lapack={0}'.format(spec['lapack'].prefix.lib),
        ]
