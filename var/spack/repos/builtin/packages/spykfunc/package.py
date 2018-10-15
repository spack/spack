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

    version('develop', git=url, submodules=True, preferred=True)

    depends_on('highfive', type='build')
    depends_on('mvdtool~mpi')

    depends_on('python@3.6:')
    depends_on('py-cython', type='run')
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('spark@2.3.2rc2', type='run')
    depends_on('hadoop@2.9.0', type='run')

    depends_on('py-bb5', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-funcsigs', type=('build', 'run'))
    depends_on('py-h5py~mpi', type=('build', 'run'))
    depends_on('py-hdfs', type=('build', 'run'))
    depends_on('py-jprops', type=('build', 'run'))
    depends_on('py-lazy-property', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-py4j@0.10.7', type=('build', 'run'))
    depends_on('py-pyarrow+parquet', type=('build', 'run'))
    depends_on('py-pyspark@2.3.2rc2', type=('build', 'run'))
    depends_on('py-sparkmanager', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        # This is a rather ugly setup to run spykfunc without having to
        # activate all python packages.
        run_env.set('HADOOP_HOME', self.spec['hadoop'].prefix)
        run_env.set('JAVA_HOME', self.spec['java'].prefix)
        run_env.set('SPARK_HOME', self.spec['spark'].prefix)

        run_env.prepend_path('PATH', os.path.join(self.spec['py-sparkmanager'].prefix, 'bin'))
        run_env.prepend_path('PATH', os.path.join(self.spec['hadoop'].prefix, 'bin'))
        run_env.prepend_path('PATH', os.path.join(self.spec['spark'].prefix, 'bin'))

        hadoop_env = dict(os.environ)
        hadoop_env['JAVA_HOME'] = self.spec['java'].prefix
        hadoop = self.spec['hadoop'].command
        hadoop_classpath = hadoop('classpath', output=str, env=hadoop_env)
        # Remove whitespaces, as they can compromise syntax in
        # module files
        hadoop_classpath = re.sub(r'[\s+]', '', hadoop_classpath)
        run_env.set('SPARK_DIST_CLASSPATH', hadoop_classpath)

        for m in spack_env.env_modifications:
            if m.name == 'PYTHONPATH':
                run_env.prepend_path('PYTHONPATH', m.value)
