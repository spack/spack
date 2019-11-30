# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob


class Tensorflow(Package):
    """TensorFlow is an Open Source Software Library for Machine Intelligence
    """

    homepage = "https://www.tensorflow.org"
    url      = "https://github.com/tensorflow/tensorflow/archive/v0.10.0.tar.gz"


    version('2.1.0-rc0',    sha256='674cc90223f1d6b7fa2969e82636a630ce453e48a9dec39d73d6dba2fd3fd243')
    version('2.0.0',        sha256='49b5f0495cd681cbcb5296a4476853d4aea19a43bdd9f179c928a977308a0617')
    version('1.15.0',       sha256='a5d49c00a175a61da7431a9b289747d62339be9cf37600330ad63b611f7f5dc9')
    version('1.14.0',       sha256='aa2a6a1daafa3af66807cfe0bc77bfe1144a9a53df9a96bab52e3e575b3047ed', preferred=True)
    version('1.13.2',       sha256='abe3bf0c47845a628b7df4c57646f41a10ee70f914f1b018a5c761be75e1f1a9')
    version('1.13.1',       sha256='7cd19978e6bc7edc2c847bce19f95515a742b34ea5e28e4389dade35348f58ed')
    version('1.12.3',       sha256='b9e5488e84f4a133ed20b18605f0cd6301f11d356bd959712db4e7b9301d0462')
    version('1.12.0',       sha256='3c87b81e37d4ed7f3da6200474fa5e656ffd20d8811068572f43610cae97ca92')
    version('1.9.0',        sha256='ffc3151b06823d57b4a408261ba8efe53601563dfe93af0866751d4f6ca5068c')
    version('1.8.0',        sha256='47646952590fd213b747247e6870d89bb4a368a95ae3561513d6c76e44f92a75')
    version('1.6.0',        sha256='03cf1423446abbead6bd8c3cf6e6affa7d99746cd119691b012aac9a1795f4fb')
    version('1.5.0',        sha256='0642781c3a3a8c2c4834b91b86aec385f0b2ada7d721571458079478cc5b29c8')
    version('1.3.0',        sha256='e1af1bb767b57c3416de0d43a5f74d174c42b85231dffd36f3630173534d4307')
    version('1.2.0',        sha256='03dbf7548d1fc1c11ed58da5fa68616f795c819f868f43478cbcaa26abed374f')
    version('1.1.0',        sha256='aad4470f52fa59f54de7b9a2da727429e6755d91d756f245f952698c42a60027')
    version('1.0.0-rc2',    sha256='bf5c58c59c182d0bdf07018f9fd394f7b760341bb432e3602874928929cf8495')
    version('0.10.0',       sha256='f32df04e8f7186aaf6723fc5396733b2f6c2fd6fe4a53a54a68b80f3ec855680')

    variant('gcp', default=False,
            description='Enable Google Cloud Platform Support')

    variant('cuda', default=True,
            description='Enable CUDA Support')

    variant('nccl', default=True,
            description='Enable NCCL Support')

    extends('python')

    depends_on('swig', type='build')

    # old tensorflow needs old bazel
    depends_on('bazel@0.27.1:0.29.1',   type='build', when='2.1.0-rc0')
    depends_on('bazel@0.24.1:0.26.1',   type='build', when='@1.15.0,2.0.0')
    depends_on('bazel@0.24.1:0.25.2',   type='build', when='@1.14.0')
    depends_on('bazel@0.19.0:0.21.0',   type='build', when='@1.13.0:1.13.2')
    depends_on('bazel@0.15.0',          type='build', when='@1.12.0:1.12.3')
    depends_on('bazel@0.10.0',          type='build', when='@1.8.0:1.9.0')
    depends_on('bazel@0.9.0',           type='build', when='@1.5.0:1.6.0')
    depends_on('bazel@0.4.5',           type='build', when='@1.2.0:1.3.0')
    depends_on('bazel@0.4.4:0.4.999',   type='build', when='@1.0.0:1.1.0')
    depends_on('bazel@0.3.1:0.4.999',   type='build', when='@:1.0.0')

    depends_on('py-absl-py@0.1.6',       type=('build', 'run'), when='@1.5.0:')
    depends_on('py-astor@0.1.6:',        type=('build', 'run'), when='@1.6.0:')
    depends_on('py-enum34@1.1.6:',       type=('build', 'run'), when='@1.5.0: ^python@:3.3')
    depends_on('py-future@0.17.1:',      type=('build', 'run'), when='@1.14.0:')
    depends_on('py-gast@0.2.0:',         type=('build', 'run'), when='@1.6.0:')
    depends_on('py-google-pasta@0.1.2:', type=('build', 'run'), when='@2.0.0:')
    depends_on('py-grpcio@1.8.6:',       type=('build', 'run'), when='@1.6.0:')
    depends_on('py-h5py',                type=('build', 'run'), when='@1.12.0:')
    depends_on('py-keras-applications@1.0.6:',  type=('build', 'run'), when='@1.12.0:')  # noqa: E501
    depends_on('py-keras-preprocessing@1.0.5:', type=('build', 'run'), when='@1.12.0:')  # noqa: E501
    depends_on('py-mock@2.0.0:',      type=('build', 'run'))
    depends_on('py-numpy@1.11.0:',    type=('build', 'run'))
    depends_on('py-protobuf@3.0.0b2', type=('build', 'run'), when='@:1.2.0')
    depends_on('py-protobuf@3.3.0:',  type=('build', 'run'), when='@1.3.0:1.6.0')        # noqa: E501
    depends_on('py-protobuf@3.6.0',   type=('build', 'run'), when='@1.8.0:')
    depends_on('py-setuptools',       type=('build', 'run'))
    depends_on('py-six@1.10.0:',      type=('build', 'run'))
    depends_on('py-termcolor@1.1.0:', type=('build', 'run'), when='@1.6.0:')
    depends_on('py-wheel',            type=('build', 'run'))

    depends_on('cuda', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('nccl', when='+nccl')

    patch('url-zlib.patch',  when='@0.10.0')
    patch('crosstool.patch', when='@1.0.0-rc2')  # also on 0.10.0 if +cuda!
    # Avoid build error: "no such package '@io_bazel_rules_docker..."
    patch('io_bazel_rules_docker2.patch', when='@1.15.0,2.0.0')
    # Avoide build error: "name 'new_http_archive' is not defined"
    patch('http_archive.patch', when='@1.12.3')

    phases = ['config', 'install']

    def setup_build_environment(self, env):
        spec = self.spec
        prefix = self.spec.prefix

        if '+gcp' in spec:
            env.set('TF_NEED_GCP','1')
        else:
            env.set('TF_NEED_GCP','0')

        env.set('PYTHON_BIN_PATH',spec['python'].command.path)
        env.set('SWIG_PATH',spec['swig'].prefix.bin)
        env.set('GCC_HOST_COMPILER_PATH',spack_cc)

        # CUDA related config options - note: tf has only been tested for cpu
        if '+cuda' in spec:
            env.set('GCC_HOST_COMPILER_PATH',self.compiler.cc) #TODO double check if this is still necessary
            env.set('TF_NEED_CUDA','1')
            env.set('TF_CUDA_VERSION',str(spec['cuda'].version.up_to(2)))
            env.set('TF_CUDNN_VERSION',str(spec['cudnn'].version)[0])
            # TODO also consider the case of cuda enabled but nccl disabled
            env.set('TF_NCCL_VERSION',str(spec['nccl'].version.up_to(1)))
            if self.spec.satisfies('@1.14.0:'):
                env.set('TF_CUDA_PATHS','"' + ','.join([str(spec['cuda'].prefix),
                                        str(spec['nccl'].prefix),
                                        str(spec['cudnn'].prefix)])+'"')
            env.set('CUDA_TOOLKIT_PATH',str(spec['cuda'].prefix))
            env.set('CUDNN_INSTALL_PATH',str(spec['cudnn'].prefix)) # ignored? as of tf@1.14.0:
            # TODO: create a string valued variant for compute capabilities?
            # one should be able to specify single or multiple capabilities
            env.set('TF_CUDA_COMPUTE_CAPABILITIES',"6.1,7.5")

            # @v1.13, config hangs without the following nccl env variables
            # however, in the end it ignores them, and sets these incorrectly
            # Because of this, these paths are reset via file filtering
            # As shown in the "post_config_fix" section
            env.set('NCCL_INSTALL_PATH',str(spec['nccl'].prefix))
            env.set('NCCL_HDR_PATH',str(spec['nccl'].prefix.include))

            env.set('TF_CUDA_CLANG','0')
            env.set('TF_NEED_ROCM','0')
            env.set('TF_NEED_TENSORRT','0')
        else:
            env.set('TF_NEED_CUDA','0')
            env.set('TF_CUDA_VERSION','')
            env.set('CUDA_TOOLKIT_PATH','')
            env.set('TF_CUDNN_VERSION','')
            env.set('CUDNN_INSTALL_PATH','')

        # config options for version 1.0
        if self.spec.satisfies('@1.0.0-rc2:'):
            env.set('CC_OPT_FLAGS','-march='+str(self.spec.target)+' -mtune='+str(self.spec.target) )
            env.set('TF_NEED_JEMALLOC','0')
            env.set('TF_NEED_HDFS','0')
            env.set('TF_ENABLE_XLA','0')
            env.set('PYTHON_LIB_PATH',self.module.site_packages_dir)
            env.set('TF_NEED_OPENCL','0')

        # additional config options starting with version 1.2
        if self.spec.satisfies('@1.2.0:'):
            env.set('TF_NEED_MKL','0')
            env.set('TF_NEED_VERBS','0')

        # additional config options starting with version 1.3
        if self.spec.satisfies('@1.3.0:'):
            env.set('TF_NEED_MPI','0')

        # additional config options starting with version 1.5
        if self.spec.satisfies('@1.5.0:'):
            env.set('TF_NEED_S3','0')
            env.set('TF_NEED_GDR','0')
            env.set('TF_NEED_OPENCL_SYCL','0')
            env.set('TF_SET_ANDROID_WORKSPACE','0')

        # additional config options starting with version 1.6
        if self.spec.satisfies('@1.6.0:'):
            env.set('TF_NEED_KAFKA','0')

        # additional config options starting with version 1.8
        if self.spec.satisfies('@1.8.0:'):
            env.set('TF_DOWNLOAD_CLANG','0')
            env.set('TF_NEED_AWS','0')

        # additional config options starting with version 1.12
        if self.spec.satisfies('@1.12.0:'):
            env.set('TF_NEED_IGNITE','0')
            env.set('TF_NEED_ROCM','0')

        # set tmpdir to a non-NFS filesystem (because bazel uses ~/.cache/bazel)        # noqa: E501
        # TODO: This should be checked for non-nfsy filesystem, but the current
        #       best idea for it is to check
        #           subprocess.call(['stat', '--file-system', '--format=%T', tmp_path]) # noqa: E501
        #       to not be nfs. This is only valid for Linux and we'd like to
        #       stay at least also OSX compatible
        tmp_path = '/tmp/spack' + '/tf'
#        tmp_path = env['SPACK_TMPDIR'] '/tmp/spack') + '/tf' #TODO
        mkdirp(tmp_path)
        env.set('TEST_TMPDIR', tmp_path)
        env.set('HOME', tmp_path)
#        env.set('CC', env['SPACK_CC']) #TODO
#        env.set('CXX', env['SPACK_CXX']) #TODO

    def config(self, spec, prefix):
        configure()

    @run_after('config')
    def post_config_fixes(self):
        spec = self.spec
        prefix = self.prefix
        if self.spec.satisfies('@1.5.0:'):
            # env variable is somehow ignored -> brute force (TODO find a better solution)
            filter_file(r'if workspace_has_any_android_rule\(\)',
                        r'if True',
                        'configure.py')

       # version dependent fixes
        if self.spec.satisfies('@1.3.0:1.5.0'):
            # checksum for protobuf that bazel downloads (@github) changed,
            # comment out to avoid error better solution: replace wrong
            # checksums in workspace.bzl
            # wrong one: 6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93,                  # noqa: E501
            # online: e5fdeee6b28cf6c38d61243adff06628baa434a22b5ebb7432d2a7fbabbdb13d                      # noqa: E501
            filter_file(r'sha256 = "6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93"',     # noqa: E501
                        r'#sha256 = "6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93"',    # noqa: E501
                        'tensorflow/workspace.bzl')
            # starting with tensorflow 1.3, tensorboard becomes a dependency
            # (...but is not really needed? Tensorboard should depend on
            # tensorflow, not the other way!)
            # -> remove from list of required packages
            filter_file(r"'tensorflow-tensorboard",
                        r"#'tensorflow-tensorboard",
                        'tensorflow/tools/pip_package/setup.py')
        if self.spec.satisfies('@1.5.0:'):
            # google cloud support seems to be installed on default, leading
            # to boringssl error manually set the flag to false to avoid
            # installing gcp support
            # (https://github.com/tensorflow/tensorflow/issues/20677#issuecomment-404634519)  # noqa: E501
            filter_file(r'--define with_gcp_support=true',
                        r'--define with_gcp_support=false',
                        '.tf_configure.bazelrc')
        if self.spec.satisfies('@1.6.0:'):
            # tensorboard name changed
            filter_file(r"'tensorboard >=",
                        r"#'tensorboard >=",
                        'tensorflow/tools/pip_package/setup.py')
        if self.spec.satisfies('@1.8.0:'):
            # 1.8.0 and 1.9.0 aborts with numpy import error during python_api
            # generation somehow the wrong PYTHONPATH is used...
            # set --distinct_host_configuration=false as a workaround
            # (https://github.com/tensorflow/tensorflow/issues/22395#issuecomment-431229451)  # noqa: E501
            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --distinct_host_configuration=false\n'
                        'build --action_env PYTHONPATH="{0}"'.format(env['PYTHONPATH']),  # noqa: E501
                        '.tf_configure.bazelrc')
        if self.spec.satisfies('@1.13.1'):
            # tensorflow_estimator is an API for tensorflow
            # tensorflow-estimator imports tensorflow during build, so
            # tensorflow has to be set up first
            filter_file(r"'tensorflow_estimator >=",
                        r"#'tensorflow_estimator >=",
                        'tensorflow/tools/pip_package/setup.py')
        if self.spec.satisfies('@2.0.0:'):
            # now it depends on the nightly versions...
            filter_file(r"'tf-estimator-nightly >=",
                        r"#'tf-estimator-nightly >=",
                        'tensorflow/tools/pip_package/setup.py')
            filter_file(r"REQUIRED_PACKAGES\[i\] = 'tb-nightly >=",
                        r"pass #REQUIRED_PACKAGES\[i\] = 'tb-nightly >=",
                        'tensorflow/tools/pip_package/setup.py')
            filter_file(r"'tb-nightly >=",
                        r"#'tb-nightly >=",
                        'tensorflow/tools/pip_package/setup.py')

        if self.spec.satisfies('@1.13.1 +nccl'):
            filter_file(r'^build --action_env NCCL_INSTALL_PATH=.*',
                     r'build --action_env NCCL_INSTALL_PATH="'+str(spec['nccl'].prefix.lib)+'"',
                     '.tf_configure.bazelrc')
            filter_file(r'^build --action_env NCCL_HDR_PATH=.*',
                     r'build --action_env NCCL_HDR_PATH="'+str(spec['nccl'].prefix.include)+'"',
                    '.tf_configure.bazelrc')

        if self.spec.satisfies('+cuda'):
            libs = [
                    str(spec['cuda'].prefix)+'/lib',
                    str(spec['cuda'].prefix)+'/lib64',
                    str(spec['cudnn'].prefix)+'/lib',
                    str(spec['cudnn'].prefix)+'/lib64',
                    str(spec['nccl'].prefix)+'/lib',
                    str(spec['nccl'].prefix)+'/lib64']
            slibs = ':'.join(libs)

            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --action_env LD_LIBRARY_PATH="'+slibs+'"',
                        '.tf_configure.bazelrc')


    def install(self, spec, prefix):
        if '+cuda' in spec:
            #TODO also consider the case '+gcp'
            #TODO make '--cxxopt...CXX11_ABI=0' a variant
            # For an explanation for ABI build option, see https://www.tensorflow.org/install/source#bazel_build_options
            # Recently noticed that TF_NEED_AWS etc environment variables aren't recognized by configure.py anymore.
            # So, explicitly disable them via bazel options.
            if self.spec.satisfies('@2.1.0-rc0'):
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',\
                    '--config=cuda', '--config=noaws', '--config=nogcp',\
                    '--config=nohdfs',\
                    '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',\
                    '--define=tensorflow_mkldnn_contraction_kernel=0',\
                    '//tensorflow/tools/pip_package:build_pip_package')
            else:
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',\
                    '--config=cuda', '--config=noaws', '--config=nogcp',\
                    '--config=nohdfs', '--config=noignite', '--config=nokafka',\
                    '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',\
                    '//tensorflow/tools/pip_package:build_pip_package')
        else:
            if self.spec.satisfies('@2.1.0-rc0'):
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',\
                    '--config=noaws', '--config=nogcp', '--config=nohdfs',\
                    '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',\
                    '--define=tensorflow_mkldnn_contraction_kernel=0',\
                    '//tensorflow/tools/pip_package:build_pip_package')
            else:
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',\
                    '--config=noaws', '--config=nogcp',\
                    '--config=nohdfs', '--config=noignite', '--config=nokafka',\
                    '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',\
                    '//tensorflow/tools/pip_package:build_pip_package')
 

        build_pip_package = Executable('bazel-bin/tensorflow/tools/pip_package/build_pip_package')  # noqa: E501
        tmp_path = env['TEST_TMPDIR']
        build_pip_package(tmp_path)

        # using setup.py for installation
        # webpage suggests: sudo pip install /tmp/tensorflow_pkg/tensorflow-0.XYZ.whl   # noqa: E501
        mkdirp('_python_build')
        cd('_python_build')
        ln = which('ln')

        for fn in glob("../bazel-bin/tensorflow/tools/pip_package/build_pip_package.runfiles/org_tensorflow/*"):  # noqa: E501
            ln('-s', fn, '.')
        for fn in glob("../tensorflow/tools/pip_package/*"):
            ln('-s', fn, '.')
        setup_py('install', '--prefix={0}'.format(prefix))
