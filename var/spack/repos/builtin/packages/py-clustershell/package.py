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


class PyClustershell(PythonPackage):
    """Scalable cluster administration Python framework - Manage node sets
    node groups and execute commands on cluster nodes in parallel.
    """

    homepage = "http://cea-hpc.github.io/clustershell/"
    url      = "https://github.com/cea-hpc/clustershell/archive/v1.8.tar.gz"

    version('1.8', sha256='ad5a13e2d107b4095229810c35365e22ea94dfd2baf4fdcfcc68ce58ee37cee3')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml')
