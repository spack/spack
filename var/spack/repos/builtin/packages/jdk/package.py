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
#
# Author: Justin Too <too1@llnl.gov>
#
import os
import distutils.dir_util
from spack import *


class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation
       in the form of a binary product aimed at Java developers.

      For legal reasons, Spack is not able to auto-download this tarball.
      To install, do as follows:
        1. Set up a Spack mirror.
        2. Manually download the JDK tarball and put it in the Spack mirror.
        3. Run `spack install`.
    """
    homepage = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

    version('8u66', '88f31f3d642c3287134297b8c10e61bf',
            url="file://%s/jdk-8u66-linux-x64.tar.gz" % os.getcwd())
    version('8u92', '65a1cc17ea362453a6e0eb4f13be76e4',
            url="file://%s/jdk-8u92-linux-x64.tar.gz" % os.getcwd())

    provides('java@8')

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.set('JAVA_HOME', self.spec.prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('JAVA_HOME', self.spec.prefix)
