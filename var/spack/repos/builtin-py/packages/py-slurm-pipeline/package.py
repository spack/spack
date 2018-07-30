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


class PySlurmPipeline(PythonPackage):
    """A Python class for scheduling SLURM jobs"""

    homepage = "https://github.com/acorg/slurm-pipeline"
    url      = "https://pypi.io/packages/source/s/slurm-pipeline/slurm-pipeline-1.1.13.tar.gz"

    version('2.0.9',  '7f97d2410db441081b79ac5c3395b8d0')
    version('1.1.13', 'd1f8c78a64718ec5e2e40ba1b6816017')

    depends_on('py-setuptools', type='build')
    # using open range although requirements*.txt give explicit versions
    # test dependencies are omitted, see #7681
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    # six only required for python 2, change when ^-dependencies work, cf #2793
    # depends_on('py-six@1.10.0:', type=('build', 'run'), when='^python@:2.8')
