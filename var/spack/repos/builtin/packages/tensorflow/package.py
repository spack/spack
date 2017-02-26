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
from llnl.util.filesystem import *


class Tensorflow(CMakePackage):
    """
    TensorFlow is an open source software library for numerical computation using data flow graphs
    """

    homepage = "https://www.tensorflow.org/"

    version('e697cf7', git='https://github.com/tensorflow/tensorflow.git', commit='e697cf787b09193a6921af6d2b7db2d6c4d2a5dd')

    depends_on('zlib')
    depends_on('giflib')
    depends_on('libpng')
    depends_on('jpeg')
    depends_on('eigen')
    depends_on('gemmlowp')
    depends_on('jsoncpp')
    depends_on('farmhash')
    depends_on('highwayhash')
    depends_on('protobuf')

    
    def mock_external(self, tfname, external_prefix):
        """TODO: Make docstring"""
        touch("CMakeFiles/%s" % tfname)
        touch("CMakeFiles/%s-complete" % tfname)
        for stamp in ("install", "mkdir", "download", 
                      "update", "patch", "configure", "build"):
            touch("{0}/src/{0}-stamp/{0}-{1}".format(tfname, stamp))
        touch("CMakeFiles/%s.dir/build.make" % tfname)
        
        install_dir = "%s/install" % tfname
        rmtree(install_dir)
        symlink(external_prefix, install_dir)

    @run_after('cmake')
    def mock_all_externals(self):
        spec = self.spec
        self.mock_external('zlib', spec['zlib'].prefix)
        self.mock_external('gif', spec['giflib'].prefix)
        self.mock_external('png', spec['libpng'].prefix)
        self.mock_external('jpeg', spec['jpeg'].prefix)
        self.mock_external('eigen', spec['eigen'].prefix)
        self.mock_external('gemmlowp', spec['gemmlowp'].prefix)
        self.mock_external('jsoncpp', spec['jsoncpp'].prefix)
        self.mock_external('farmhash', spec['farmhash'].prefix)
        self.mock_external('highwayhash', spec['highwayhash'].prefix)
        self.mock_external('protobuf', spec['protobuf'].prefix)
