# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob
import os


class Tensorflow(Package):
    """TensorFlow is an Open Source Software Library for Machine Intelligence"""

    homepage = "https://www.tensorflow.org"
    url      = "https://github.com/tensorflow/tensorflow/archive/v0.10.0.tar.gz"

    version('1.13.1',    sha256='7cd19978e6bc7edc2c847bce19f95515a742b34ea5e28e4389dade35348f58ed')
    version('1.12.0',    '48164180a2573e75f1c8dff492a550a0', preferred=True)
    version('1.9.0',     '3426192cce0f8e070b2010e5bd5695cd')
    version('1.8.0',     'cd45874be9296644471dd43e7da3fbd0')
    version('1.6.0',     '6dc60ac37e49427cd7069968da42c1ac')
    version('1.5.0',     'e087dc1f47dbbda87cf4278acddf785b')
    version('1.3.0',     '01c008c58d206324ef68cd5116a83965')
    version('1.2.0',     '3f15746caabfd2583724258643fd1678')
    version('1.1.0',     'fb745649d33954c97d29b7acaffe7d65')
    version('0.10.0',    'b75cbd494d61a809af5ef25d7fba561b')

    depends_on('swig',                          type='build')

    # old tensorflow needs old bazel
    depends_on('bazel@0.19.2',                  type='build',          when='@1.13.1')
    depends_on('bazel@0.15.0',                  type='build',          when='@1.12.0')
    depends_on('bazel@0.10.0',                  type='build',          when='@1.8.0:1.9.0')
    depends_on('bazel@0.9.0',                   type='build',          when='@1.5.0:1.6.0')
    depends_on('bazel@0.4.5',                   type='build',          when='@1.2.0:1.3.0')
    depends_on('bazel@0.4.4:0.4.999',           type='build',          when='@1.0.0:1.1.0')
    depends_on('bazel@0.3.1:0.4.999',           type='build',          when='@:1.0.0')

    extends('python')
    depends_on('py-setuptools',                 type=('build', 'run'))
    depends_on('py-numpy@1.11.0:',              type=('build', 'run'))
    depends_on('py-six@1.10.0:',                type=('build', 'run'))

    depends_on('py-protobuf@3.6.1',             type=('build', 'run'), when='@1.8.0:')
    depends_on('py-protobuf@3.3.0:',            type=('build', 'run'), when='@1.3.0:1.6.0')
    depends_on('py-protobuf@3.0.0b2',           type=('build', 'run'), when='@:1.2.0')

    depends_on('py-wheel',                      type=('build', 'run'))
    depends_on('py-mock@2.0.0:',                type=('build', 'run'))

    depends_on('py-enum34@1.1.6:',              type=('build', 'run'), when='@1.5.0:^python@:3.3.99')
    depends_on('py-absl-py@0.1.6',              type=('build', 'run'), when='@1.5.0:')

    depends_on('py-astor@0.1.6:',               type=('build', 'run'), when='@1.6.0:')
    depends_on('py-gast@0.2.0:',                type=('build', 'run'), when='@1.6.0:')
    depends_on('py-grpcio@1.8.6:',              type=('build', 'run'), when='@1.6.0:')
    depends_on('py-termcolor@1.1.0:',           type=('build', 'run'), when='@1.6.0:')

    depends_on('py-keras-applications@1.0.6:',  type=('build', 'run'), when='@1.12.0:')
    depends_on('py-keras-preprocessing@1.0.5:', type=('build', 'run'), when='@1.12.0:')
    depends_on('py-h5py~mpi',                   type=('build', 'run'), when='@1.12.0:')

    patch('url-zlib.patch',  when='@0.10.0')

    variant('gcp', default=False,
            description='Enable Google Cloud Platform Support')

    variant('cuda', default=False,
            description='Enable CUDA Support')

    variant('deployment_build', default='1',  description='Build number for re-builds')

    depends_on('cuda', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('nccl', when='+cuda')


    def install(self, spec, prefix):
        configure()
        spec = self.spec

        # set swig path in install instead of setup_environment as
        # it could be external and not accessible while module refresh
        env['SWIG_PATH'] = str(spec['swig'].prefix.bin)

        # version dependent fixes
        if spec.satisfies('@1.3.0:1.5.0'):
            # checksum for protobuf that bazel downloads (@github) changed, comment out to avoid error
            # better solution: replace wrong checksums in workspace.bzl
            # wrong one: 6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93,
            # online: e5fdeee6b28cf6c38d61243adff06628baa434a22b5ebb7432d2a7fbabbdb13d
            filter_file(r'sha256 = "6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93"',
                        r'#sha256 = "6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93"',
                        'tensorflow/workspace.bzl')
            # starting with tensorflow 1.3, tensorboard becomes a dependency
            # (...but is not really needed? Tensorboard should depend on tensorflow, not the other way!)
            # -> remove from list of required packages
            filter_file(r"'tensorflow-tensorboard",
                        r"#'tensorflow-tensorboard",
                        'tensorflow/tools/pip_package/setup.py')
        if spec.satisfies('@1.5.0:'):
            # google cloud support seems to be installed on default, leading to boringssl error
            # manually set the flag to false to avoid installing gcp support
            # (https://github.com/tensorflow/tensorflow/issues/20677#issuecomment-404634519)
            filter_file(r'--define with_gcp_support=true',
                        r'--define with_gcp_support=false',
                        '.tf_configure.bazelrc')
        if spec.satisfies('@1.6.0:'):
            # tensorboard name changed
            filter_file(r"'tensorboard >=",
                        r"#'tensorboard >=",
                        'tensorflow/tools/pip_package/setup.py')
        if spec.satisfies('@1.8.0:'):
            # 1.8.0 and 1.9.0 aborts with numpy import error during python_api generation
            # somehow the wrong PYTHONPATH is used...set --distinct_host_configuration=false as a workaround
            # (https://github.com/tensorflow/tensorflow/issues/22395#issuecomment-431229451)
            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --distinct_host_configuration=false\n'
                        'build --action_env PYTHONPATH="{}"'.format(env['PYTHONPATH']),
                        '.tf_configure.bazelrc')

        if spec.satisfies('@1.12.0:'):
            # add link to spack-installed openssl libs (needed if no system openssl available)
            filter_file('-lssl', '-lssl '+spec['openssl'].libs.search_flags, 'third_party/systemlibs/boringssl.BUILD')
            filter_file('-lcrypto', '-lcrypto '+spec['openssl'].libs.search_flags, 'third_party/systemlibs/boringssl.BUILD')

        if '+cuda' in spec:
            # Note : do not enable skylake yet, see https://github.com/easybuilders/easybuild-easyconfigs/issues/5936
            # get path for all dependent libraries to avoid issue with linking especially cuda and cudnn
            ld_lib_path = env.get('LD_LIBRARY_PATH')
            bazel('-c', 'opt', '--copt=-mavx2', '--copt=-msse4.2', '--copt=-mfma', '--copt=-mavx', '--copt=-mfpmath=both', '--config=cuda', '--action_env="LD_LIBRARY_PATH=%s"' % ld_lib_path,  '//tensorflow/tools/pip_package:build_pip_package')
        else:
            bazel('-c', 'opt', '--copt=-mavx2', '--copt=-msse4.2', '--copt=-mfma', '--copt=-mavx', '--copt=-mfpmath=both', '--config=mkl', '//tensorflow/tools/pip_package:build_pip_package')

        build_pip_package = Executable('bazel-bin/tensorflow/tools/pip_package/build_pip_package')
        build_pip_package('.')

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


    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        # add libcuda.so to LD_LIBRARY_PATH as build can be triggered on the node without cuda driver
        #if '+cuda' in spec:
        #    spack_env.prepend_path('LD_LIBRARY_PATH', spec['cuda'].prefix.lib64.stubs)

        if '+gcp' in spec:
            spack_env.set('TF_NEED_GCP', '1')
        else:
            spack_env.set('TF_NEED_GCP', '0')

        spack_env.set('PYTHON_BIN_PATH', str(spec['python'].prefix.bin) + '/python')
        spack_env.set('PYTHONUSERBASE', str(spec['python'].prefix))
        spack_env.set('USE_DEFAULT_PYTHON_LIB_PATH', '1')
        spack_env.set('GCC_HOST_COMPILER_PATH', spack_cc)

        spack_env.set('TF_ENABLE_XLA', '0')

        if '+cuda' in spec:
            spack_env.set('TF_NEED_CUDA', '1')
            spack_env.set('TF_CUDA_CLANG', '0')
            spack_env.set('TF_NEED_TENSORRT', '0')
            spack_env.set('TF_CUDA_VERSION', str(spec['cuda'].version))
            spack_env.set('CUDA_TOOLKIT_PATH', str(spec['cuda'].prefix))
            spack_env.set('TF_CUDNN_VERSION', str(spec['cudnn'].version)[0])
            spack_env.set('CUDNN_INSTALL_PATH', str(spec['cudnn'].prefix))
            spack_env.set('NCCL_INSTALL_PATH', str(spec['nccl'].prefix))
            spack_env.set('TF_NCCL_VERSION', str(spec['nccl'].version)[0])
            spack_env.set('TF_CUDA_COMPUTE_CAPABILITIES', '6.0,6.1,7.0')
        else:
            spack_env.set('TF_NEED_CUDA', '0')
            spack_env.set('TF_CUDA_VERSION', '')
            spack_env.set('CUDA_TOOLKIT_PATH', '')
            spack_env.set('TF_CUDNN_VERSION', '')
            spack_env.set('CUDNN_INSTALL_PATH', '')

        # additional config options starting with version 1.2
        if spec.satisfies('@1.2.0:'):
            spack_env.set('TF_NEED_MKL', '1')
            spack_env.set('TF_NEED_VERBS', '1')

        # additional config options starting with version 1.3
        if spec.satisfies('@1.3.0:'):
            spack_env.set('TF_NEED_MPI', '0')

        # additional config options starting with version 1.5
        if spec.satisfies('@1.5.0:'):
            spack_env.set('TF_NEED_S3', '0')
            spack_env.set('TF_NEED_GDR', '0')
            spack_env.set('TF_NEED_OPENCL_SYCL', '0')
            spack_env.set('TF_SET_ANDROID_WORKSPACE', '0')
            # env variable is somehow ignored -> brute force
            # filter_file(r'if workspace_has_any_android_rule\(\)', r'if True', 'configure.py')

        # additional config options starting with version 1.6
        if spec.satisfies('@1.6.0:'):
            spack_env.set('TF_NEED_KAFKA', '0')

        # additional config options starting with version 1.8
        if spec.satisfies('@1.8.0:'):
            spack_env.set('TF_DOWNLOAD_CLANG', '0')
            spack_env.set('TF_NEED_AWS', '0')

        # boringssl error again, build against openssl instead via TF_SYSTEM_LIBS
        # does not work for tf < 1.12.0
        # (https://github.com/tensorflow/tensorflow/issues/25283#issuecomment-460124556)
        if spec.satisfies('@1.12.0:'):
            spack_env.set('TF_SYSTEM_LIBS', "boringssl")
            spack_env.set('TF_NEED_IGNITE', '0')
            spack_env.set('TF_NEED_ROCM', '0')
