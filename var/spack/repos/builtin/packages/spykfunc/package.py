##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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
import os
import re

from spack import *


class Spykfunc(PythonPackage):
    """Spykfunc - Spark functionalizer developed by Blue Brain Project, EPFL
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/Spykfunc"
    url      = "ssh://bbpcode.epfl.ch/building/Spykfunc"

    version('develop', git=url, submodules=True, clean=False)
    version('0.11.0', git=url, tag='v0.11.0', submodules=True, clean=False)
    version('0.12.0', git=url, tag='v0.12.0', submodules=True, clean=False)
    version('0.12.1', git=url, tag='v0.12.1', submodules=True, clean=False)
    version('0.12.2', git=url, tag='v0.12.2', submodules=True, clean=False)
    version('0.13.0', git=url, tag='v0.13.0', submodules=True, clean=False)
    version('0.13.1', git=url, tag='v0.13.1', submodules=True, clean=False)
    version('0.13.2', git=url, tag='v0.13.2', submodules=True, clean=False)
    version('0.14.1', git=url, tag='v0.14.1', submodules=True, clean=False)
    version('0.14.2', git=url, tag='v0.14.2', submodules=True, clean=False)
    version('0.14.3', git=url, tag='v0.14.3', submodules=True, clean=False)

    depends_on('hdf5~mpi')
    depends_on('highfive~mpi', type='build')

    # Note : when spark is used as external package, spec['java'] is not
    # accessible. Add explicit dependency for now.
    depends_on('java@8', type=('build', 'run'))

    depends_on('mvdtool~mpi', when='@:0.13.1')
    depends_on('mvdtool~mpi+python', type=('build', 'run'), when='@0.13.2:0.14.3')
    depends_on('py-mvdtool', type=('build', 'run'), when='@0.14.4:')

    depends_on('python@3.6:')
    depends_on('py-cython', type='run')
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('spark+hadoop@2.3.2rc2:', type='run')
    depends_on('hadoop@:2.999', type='run')

    depends_on('py-bb5', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-funcsigs', type=('build', 'run'))
    depends_on('py-h5py~mpi', type=('build', 'run'))
    depends_on('py-hdfs', type=('build', 'run'))
    depends_on('py-jprops', type=('build', 'run'))
    depends_on('py-lazy-property', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-morphio@2.1.2:', type=('build', 'run'), when='@0.14.4:')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-pyarrow+parquet', type=('build', 'run'))
    depends_on('py-pyspark@2.3.2rc2:', type=('build', 'run'))
    depends_on('py-sparkmanager', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        # This is a rather ugly setup to run spykfunc without having to
        # activate all python packages.
        run_env.set('JAVA_HOME', self.spec['java'].prefix)
        run_env.set('SPARK_HOME', self.spec['spark'].prefix)
        run_env.set('HADOOP_HOME', self.spec['hadoop'].prefix)

        run_env.prepend_path('PATH', os.path.join(self.spec['py-bb5'].prefix, 'bin'))
        run_env.prepend_path('PATH', os.path.join(self.spec['py-sparkmanager'].prefix, 'bin'))
        run_env.prepend_path('PATH', os.path.join(self.spec['spark'].prefix, 'bin'))
