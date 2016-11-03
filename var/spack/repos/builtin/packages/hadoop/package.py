##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Alfredo Gimenez, gimenez1@llnl.gov, All rights reserved.
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


class Hadoop(Package):
    """The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models.
    """

    homepage = "http://hadoop.apache.org/"
    url      = "http://mirrors.ocf.berkeley.edu/apache/hadoop/common/hadoop-2.6.4/hadoop-2.6.4.tar.gz"

    version('2.6.4', '37019f13d7dcd819727be158440b9442')

    depends_on('jdk', type='run')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('etc')
        install_dir('include')
        install_dir('lib')
        install_dir('libexec')
        install_dir('sbin')
        install_dir('share')
