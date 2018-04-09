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
import shutil
import subprocess
import glob


class Xgboost(Package):
    """
    XGBoost is an optimized distributed gradient boosting library designed to
    be highly efficient, flexible and portable. It implements machine learning
    algorithms under the Gradient Boosting framework. XGBoost provides a
    parallel tree boosting (also known as GBDT, GBM) that solve many data
    science problems in a fast and accurate way. The same code runs on major
    distributed environment (Hadoop, SGE, MPI) and can solve problems beyond
    billions of examples.
    """

    homepage = "http://xgboost.readthedocs.io/en/latest/"
    url      = "https://github.com/dmlc/xgboost"

    version('0.7', commit='4aa346c', git="https://github.com/dmlc/xgboost", submodules=True)

    variant('jvm-packages', default=False,
            description='jvm-packages are compiled')

    variant('gpu', default=False,
            description='compiled with GPU support')

    depends_on('cmake', type='build')

    depends_on('maven', type='build', when='+jvm-packages')
    depends_on('jdk', type='build', when='+jvm-packages')

    depends_on('cuda', type='build', when='+gpu')

    conflicts('%gcc@:4.7.4')

    def install(self, spec, prefix):
        if '+gpu' in spec:
            cmake('-DUSE_CUDA=ON')
            # get back to xgboost dir to make
            os.chdir(str(self.stage.source_path))
        make()

        # no bin directory under xgboost, so create one
        os.mkdir('bin')
        # move what seems to be the only executable under bin
        shutil.copy('xgboost', 'bin/xgboost')
        install_tree('lib', prefix.lib)
        install_tree('bin', prefix.bin)

        # make jvm-packages
        if '+jvm-packages' in spec:
            os.chdir('jvm-packages')
            # custom repo location.
            # Default is ~/.m2, and directory structure goes
            # like ~/.m2/repository/ml/dmlc/...  as opposed to m2/ml/dmlc/...
            mvn_repo = str(self.stage.source_path) + '/jvm-packages/m2'
            drepo = '-Dmaven.repo.local=' + mvn_repo
            # compile with maven
            subprocess.call(['mvn', drepo, 'install', '-DskipTests'])
            # a more strict option to skip tests is '-Dmaven.test.skip=true'
            # To unskip tests, do:
            # subprocess.call(['mvn', drepo, 'install'])

            # put usefull xgboost jars under package prefix
            ver = str(self.spec.version)
            for xgtype in ['', '-spark', '-flink', '-example']:
                ujars = glob.glob(mvn_repo + '/ml/dmlc/xgboost4j' + xgtype +
                                  '/' + ver + '/*.jar')
                for jar in ujars:
                    shutil.copyfile(jar, str(spec.prefix) + '/' +
                                    os.path.basename(jar))
