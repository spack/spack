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
import os


class Cistem(AutotoolsPackage):
    """cisTEM is user-friendly software to process cryo-EM images of
       macromolecular complexes and obtain high-resolution 3D reconstructions
       from them."""

    homepage = "https://cistem.org/"

    version('1.0.0', sha256='c62068f53d0a269ffa1bfff34641597d3795989a930686437fba9eed7a991af6')

    def url_for_version(self, version):
        c_file = "file://{0}/cistem-{1}-beta-source-code.tar.gz"
        return c_file.format(os.getcwd(), version)

    depends_on('wx@3.0.2')
    depends_on('fftw')
