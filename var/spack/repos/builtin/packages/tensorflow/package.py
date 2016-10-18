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
from glob import glob

class Tensorflow(Package):
    """TensorFlow is an Open Source Software Library for Machine Intelligence"""

    homepage = "https://www.tensorflow.org"
    url = "https://github.com/tensorflow/tensorflow/archive/v0.10.0.tar.gz"

    version('0.10.0', 'b75cbd494d61a809af5ef25d7fba561b')

    depends_on('bazel@0.3.1:',         type='build')
    depends_on('swig',                 type='build')

    extends('python')
    depends_on('py-numpy@1.8.2:',      type=nolink)
    depends_on('py-six@1.10.0:',       type=nolink)
    depends_on('py-protobuf@3.0.0b2:', type=nolink)
    depends_on('py-wheel',             type=nolink)
    depends_on('py-mock@2.0.0:',       type=nolink)

    # FIXME: tensorflow pulls in a lot more dependencies...
    # cf. WORKSPACE file

    variant('gcp', default=False,
            description='Enable Google Cloud Platform Support')

    variant('cuda', default=False,
            description='Enable CUDA Support')

    depends_on('cuda', when='+cuda')

    def install(self, spec, prefix):
        # tensorflow's configure script works in non-interactive mode
        # if all environment variables are set before starting the script
        if '+gcp' in spec:
            env['TF_NEED_GCP'] = '1'
        else:
            env['TF_NEED_GCP'] = '0'
        env['PYTHON_BIN_PATH'] = str(which('python'))
        env['SWIG_PATH'] = str(which('swig'))
        env['GCC_HOST_COMPILER_PATH'] = str(which('gcc'))

        assert '~cuda' in spec # FIXME
        if '+cuda' in spec:
            env['TF_NEED_CUDA'] = '1'
        else:
            env['TF_NEED_CUDA'] = '0'

        # FIXME: needed for cuda!
        env['TF_CUDA_VERSION'] = '' # FIXME spec['cuda'].version ?
        env['CUDA_TOOLKIT_PATH'] = '' # FIXME spec['cuda'].prefix ?
        env['TF_CUDNN_VERSION'] = ''
        env['CUDNN_INSTALL_PATH'] = ''

        configure()
        if '+cuda' in spec:
            bazel('-c', 'opt', '--config=cuda', '//tensorflow/tools/pip_package:build_pip_package')
        else:
            bazel('-c', 'opt', '//tensorflow/tools/pip_package:build_pip_package')

        build_pip_package = Executable('bazel-bin/tensorflow/tools/pip_package/build_pip_package')
        build_pip_package('%s/tmp_tensorflow_pkg' % self.stage.path)

        # using setup.py for installation
        # webpage suggests: sudo pip install /tmp/tensorflow_pkg/tensorflow-0.XYZ.whl
        mkdirp('_python_build')
        cd('_python_build')
        ln = which('ln')

        for fn in glob("../bazel-bin/tensorflow/tools/pip_package/build_pip_package.runfiles/org_tensorflow/*"):
            ln('-s', fn, '.')
        for fn in glob("../tensorflow/tools/pip_package/*"):
            ln('-s', fn, '.')
        setup_py('install', '--prefix={0}'.format(prefix))
