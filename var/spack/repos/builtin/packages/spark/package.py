##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import shutil


class Spark(Package):
    """Apache Spark is a fast and general engine
    for large-scale data processing.
    """

    homepage = "http://spark.apache.org"
    url      = "http://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-without-hadoop.tgz"

    variant('hadoop', default=False,
            description='Build with Hadoop')

    depends_on('jdk', type=('build', 'run'))
    depends_on('hadoop', when='+hadoop', type=('build', 'run'))

    version('2.1.0', '21d4471e78250775b1fa7c0e6c3a1326')
    version('2.0.2', '32110c1bb8f081359738742bd26bced1')
    version('2.0.0', '8a5307d973da6949a385aefb6ff747bb')
    version('1.6.2', '304394fbe2899211217f0cd9e9b2b5d9')
    version('1.6.1', 'fcf4961649f15af1fea78c882e65b001')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('conf')
        install_dir('jars')
        install_dir('python')
        install_dir('R')
        install_dir('sbin')
        install_dir('yarn')

        # required for spark to recognize binary distribution
        shutil.copy('RELEASE', prefix)

    @when('+hadoop')
    def setup_environment(self, spack_env, run_env):

        env['JAVA_HOME'] = self.spec['jdk'].prefix
        # spack_env.set('JAVA_HOME', self.spec['jdk'].prefix)

        hadoop_bin_path = join_path(self.spec['hadoop'].prefix.bin, 'hadoop')
        hadoop_bin = Executable(hadoop_bin_path)
        hadoop_classpath = hadoop_bin('classpath', return_output=True)

        run_env.set('SPARK_DIST_CLASSPATH', hadoop_classpath)
