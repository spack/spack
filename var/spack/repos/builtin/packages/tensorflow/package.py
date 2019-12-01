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

    maintainers = ['adamjstewart']

    version('2.1.0-rc0', sha256='674cc90223f1d6b7fa2969e82636a630ce453e48a9dec39d73d6dba2fd3fd243')
    version('2.0.0',  sha256='49b5f0495cd681cbcb5296a4476853d4aea19a43bdd9f179c928a977308a0617')
    version('1.15.0', sha256='a5d49c00a175a61da7431a9b289747d62339be9cf37600330ad63b611f7f5dc9')
    version('1.14.0', sha256='aa2a6a1daafa3af66807cfe0bc77bfe1144a9a53df9a96bab52e3e575b3047ed', preferred=True)
    version('1.13.2', sha256='abe3bf0c47845a628b7df4c57646f41a10ee70f914f1b018a5c761be75e1f1a9')
    version('1.13.1', sha256='7cd19978e6bc7edc2c847bce19f95515a742b34ea5e28e4389dade35348f58ed')
    version('1.12.3', sha256='b9e5488e84f4a133ed20b18605f0cd6301f11d356bd959712db4e7b9301d0462')
    version('1.12.2', sha256='90ffc7cf1df5e4b8385c9108db18d5d5034ec423547c0e167d44f5746a20d06b')
    version('1.12.1', sha256='7b559a3ae56322b7a7e4307f45f9fce96022c533a98b32c18bfdff8c5838271d')
    version('1.12.0', sha256='3c87b81e37d4ed7f3da6200474fa5e656ffd20d8811068572f43610cae97ca92')
    version('1.11.0', sha256='f49ce3f1d04cee854bc9f74fa9696991140b34a2e2447f35f01391b72c8bfa9f')
    version('1.10.1', sha256='83092d709800e2d93d4d4b1bcacaeb74f2f328962ed764cb35bbee20402879c6')
    version('1.10.0', sha256='ee9cb98d9e0d8106f2f4ed52a38fe89399324af303e1401567e5b64a9f86744b')
    version('1.9.0',  sha256='ffc3151b06823d57b4a408261ba8efe53601563dfe93af0866751d4f6ca5068c')
    version('1.8.0',  sha256='47646952590fd213b747247e6870d89bb4a368a95ae3561513d6c76e44f92a75')
    version('1.7.1',  sha256='3147f8c60d1f30da23a831bcf732e74b935dcee7c62e4b8b85f0f093030b52c8')
    version('1.7.0',  sha256='c676a96fc8700722816b2b98c85578b2f99fac7a7b2484c9c7f0641484f8d50d')
    version('1.6.0',  sha256='03cf1423446abbead6bd8c3cf6e6affa7d99746cd119691b012aac9a1795f4fb')
    version('1.5.1',  sha256='cab2157783905e12a7a3baae3264edfb739dd92d5658019a131fff4b14190240')
    version('1.5.0',  sha256='0642781c3a3a8c2c4834b91b86aec385f0b2ada7d721571458079478cc5b29c8')
    version('1.4.1',  sha256='1f75e463318419a1b3ae076d5a92697c1d3a85e8377c946a5510b651ff5c0d60')
    version('1.4.0',  sha256='8a0ad8d61f8f6c0282c548661994a5ab83ac531bac496c3041dedc1ab021107b')
    version('1.3.1',  sha256='ded509c209f8a1d390df8a2f44be5b5c29963172b0e0f095304efb59765d0523')
    version('1.3.0',  sha256='e1af1bb767b57c3416de0d43a5f74d174c42b85231dffd36f3630173534d4307')
    version('1.2.1',  sha256='f2baf09b1a9a0500907b4d5cb5473070b3ecede06ed6e8d1096873c91922fb9e')
    version('1.2.0',  sha256='03dbf7548d1fc1c11ed58da5fa68616f795c819f868f43478cbcaa26abed374f')
    version('1.1.0',  sha256='aad4470f52fa59f54de7b9a2da727429e6755d91d756f245f952698c42a60027')
    version('1.0.1',  sha256='deea3c65e0703da96d9c3f1162e464c51d37659dd129396af134e9e8f1ea8c05')
    version('1.0.0',  sha256='db8b3b8f4134b7c9c1b4165492ad5d5bb78889fcd99ffdffc325e97da3e8c677')
    version('0.12.0', sha256='13a1d4e98c82eae7e26fe75384de1517d6126f63ba5d302392ec02ac3ae4b1b9')
    version('0.11.0', sha256='24242ff696234bb1e58d09d45169b148525ccb706f980a4a92ddd3b82c7546dc')
    version('0.10.0', sha256='f32df04e8f7186aaf6723fc5396733b2f6c2fd6fe4a53a54a68b80f3ec855680')
    version('0.9.0',  sha256='3128c396af19518c642d3e590212291e1d93c5b047472a10cf3245b53adac9c9')
    version('0.8.0',  sha256='f201ba7fb7609a6416968d4e1920d87d67be693b5bc7d34b6b4a79860a9a8a4e')
    version('0.7.1',  sha256='ef34121432f7a522cf9f99a56cdd86e370cc5fa3ee31255ca7cb17f36b8dfc0d')
    version('0.7.0',  sha256='43dd3051f947aa66e6fc09dac2f86a2efe2e019736bbd091c138544b86d717ce')
    version('0.6.0',  sha256='f86ace45e99053b09749cd55ab79c57274d8c7460ae763c5e808d81ffbc3b657')

    variant('gcp', default=False,
            description='Enable Google Cloud Platform Support')
    variant('cuda', default=True, description='Enable CUDA Support')
    variant('nccl', default=True, description='Enable NCCL Support')

    extends('python')

    depends_on('swig', type='build')

    # See _TF_MIN_BAZEL_VERSION and _TF_MAX_BAZEL_VERSION in configure.py
    depends_on('bazel@0.27.1:0.29.1', type='build', when='@2.1:')
    depends_on('bazel@0.24.1:0.26.1', type='build', when='@1.15:2.0')
    # See call to check_bazel_version in configure.py
    depends_on('bazel@0.24.1:0.25.2', type='build', when='@1.14.0')
    depends_on('bazel@0.19.0:0.21.0', type='build', when='@1.13.0:1.13.2')
    depends_on('bazel@0.24.1:0.25.0', type='build', when='@1.12.1')
    depends_on('bazel@0.15.0',        type='build', when='@1.10:1.12.0,1.12.2:1.12.3')
    depends_on('bazel@0.10.0',        type='build', when='@1.8:1.9')
    # See call to check_version in tensorflow/workspace.bzl
    depends_on('bazel@0.5.4',         type='build', when='@1.4:1.6')
    # See MIN_BAZEL_VERSION in configure
    depends_on('bazel@0.4.5:',        type='build', when='@1.2:1.3')
    # See call to check_version in WORKSPACE
    depends_on('bazel@0.4.2:',        type='build', when='@1.0:1.1')
    depends_on('bazel@0.3.2:',        type='build', when='@0.12.0:0.12.1')
    depends_on('bazel@0.3.0:',        type='build', when='@0.11.0')
    depends_on('bazel@0.2.0:',        type='build', when='@0.9:0.10')
    depends_on('bazel@0.1.4:',        type='build', when='@0.8.0')
    depends_on('bazel',               type='build', when='@:0.7')

    depends_on('py-absl-py@0.1.6',       type=('build', 'run'), when='@1.5.0:')
    depends_on('py-astor@0.1.6:',        type=('build', 'run'), when='@1.6.0:')
    depends_on('py-enum34@1.1.6:',       type=('build', 'run'), when='@1.5.0: ^python@:3.3')
    depends_on('py-future@0.17.1:',      type=('build', 'run'), when='@1.14.0:')
    depends_on('py-gast@0.2.0:',         type=('build', 'run'), when='@1.6.0:')
    depends_on('py-google-pasta@0.1.2:', type=('build', 'run'), when='@2.0.0:')
    depends_on('py-grpcio@1.8.6:',       type=('build', 'run'), when='@1.6.0:')
    depends_on('py-h5py',                type=('build', 'run'), when='@1.12.0:')
    depends_on('py-keras-applications@1.0.6:',  type=('build', 'run'), when='@1.12.0:')
    depends_on('py-keras-preprocessing@1.0.5:', type=('build', 'run'), when='@1.12.0:')
    depends_on('py-mock@2.0.0:',      type=('build', 'run'))
    depends_on('py-numpy@1.11.0:',    type=('build', 'run'))
    depends_on('py-protobuf@3.0.0b2', type=('build', 'run'), when='@:1.2.0')
    depends_on('py-protobuf@3.3.0:',  type=('build', 'run'), when='@1.3.0:1.6.0')
    depends_on('py-protobuf@3.6.0',   type=('build', 'run'), when='@1.8.0:')
    depends_on('py-setuptools',       type=('build', 'run'))
    depends_on('py-six@1.10.0:',      type=('build', 'run'))
    depends_on('py-termcolor@1.1.0:', type=('build', 'run'), when='@1.6.0:')
    depends_on('py-wheel',            type=('build', 'run'))

    depends_on('cuda', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('nccl', when='+nccl')

    patch('url-zlib.patch',  when='@0.10.0')
    patch('crosstool.patch', when='@0.10.0+cuda')
    # Avoid build error: "no such package '@io_bazel_rules_docker..."
    patch('io_bazel_rules_docker2.patch', when='@1.15.0,2.0.0')
    # Avoide build error: "name 'new_http_archive' is not defined"
    patch('http_archive.patch', when='@1.12.3')

    phases = ['configure', 'build', 'install']

    # https://www.tensorflow.org/install/source
    def setup_build_environment(self, env):
        spec = self.spec

        if '+gcp' in spec:
            env.set('TF_NEED_GCP', '1')
        else:
            env.set('TF_NEED_GCP', '0')

        env.set('PYTHON_BIN_PATH', spec['python'].command.path)
        env.set('SWIG_PATH', spec['swig'].prefix.bin)
        env.set('GCC_HOST_COMPILER_PATH', spack_cc)
        env.set('TF_CONFIGURE_IOS', '0')

        # CUDA related configure options
        if '+cuda' in spec:
            env.set('GCC_HOST_COMPILER_PATH', self.compiler.cc)
            env.set('TF_NEED_CUDA', '1')
            env.set('TF_CUDA_VERSION', spec['cuda'].version.up_to(2))
            env.set('TF_CUDNN_VERSION', spec['cudnn'].version.up_to(1))
            # TODO also consider the case of cuda enabled but nccl disabled
            env.set('TF_NCCL_VERSION', spec['nccl'].version.up_to(1))
            if self.spec.satisfies('@1.14.0:'):
                env.set('TF_CUDA_PATHS', ','.join([
                    spec['cuda'].prefix,
                    spec['nccl'].prefix,
                    spec['cudnn'].prefix,
                ]))
            env.set('CUDA_TOOLKIT_PATH', spec['cuda'].prefix)
            # ignored? as of tf@1.14.0:
            env.set('CUDNN_INSTALL_PATH', spec['cudnn'].prefix)
            # TODO: create a string valued variant for compute capabilities?
            # one should be able to specify single or multiple capabilities
            env.set('TF_CUDA_COMPUTE_CAPABILITIES', "6.1,7.5")

            # @v1.13, configure hangs without the following nccl env variables
            # however, in the end it ignores them, and sets these incorrectly
            # Because of this, these paths are reset via file filtering
            # As shown in the "post_configure_fix" section
            env.set('NCCL_INSTALL_PATH', spec['nccl'].prefix)
            env.set('NCCL_HDR_PATH', spec['nccl'].prefix.include)

            env.set('TF_CUDA_CLANG', '0')
            env.set('TF_NEED_ROCM', '0')
            env.set('TF_NEED_TENSORRT', '0')
        else:
            env.set('TF_NEED_CUDA', '0')
            env.set('TF_CUDA_VERSION', '')
            env.set('CUDA_TOOLKIT_PATH', '')
            env.set('TF_CUDNN_VERSION', '')
            env.set('CUDNN_INSTALL_PATH', '')

        # configure options for version 1.0
        if self.spec.satisfies('@1.0.0:'):
            # TODO: this env var must be set, can we query Spack to find out
            # what optimization flags it automatically adds?
            env.set('CC_OPT_FLAGS', '-march=native -Wno-sign-compare')
            env.set('TF_NEED_JEMALLOC', '0')
            env.set('TF_NEED_HDFS', '0')
            env.set('TF_ENABLE_XLA', '0')
            env.set('PYTHON_LIB_PATH', self.module.site_packages_dir)
            env.set('TF_NEED_OPENCL', '0')

        # additional configure options starting with version 1.2
        if self.spec.satisfies('@1.2.0:'):
            env.set('TF_NEED_MKL', '0')
            env.set('TF_NEED_VERBS', '0')

        # additional configure options starting with version 1.3
        if self.spec.satisfies('@1.3.0:'):
            env.set('TF_NEED_MPI', '0')

        # additional configure options starting with version 1.5
        if self.spec.satisfies('@1.5.0:'):
            env.set('TF_NEED_S3', '0')
            env.set('TF_NEED_GDR', '0')
            env.set('TF_NEED_OPENCL_SYCL', '0')
            env.set('TF_SET_ANDROID_WORKSPACE', '0')

        # additional configure options starting with version 1.6
        if self.spec.satisfies('@1.6.0:'):
            env.set('TF_NEED_KAFKA', '0')

        # additional configure options starting with version 1.8
        if self.spec.satisfies('@1.8.0:'):
            env.set('TF_DOWNLOAD_CLANG', '0')
            env.set('TF_NEED_AWS', '0')

        # additional configure options starting with version 1.12
        if self.spec.satisfies('@1.12.0:'):
            env.set('TF_NEED_IGNITE', '0')
            env.set('TF_NEED_ROCM', '0')

        # set tmpdir to a non-NFS filesystem
        # (because bazel uses ~/.cache/bazel)
        # TODO: This should be checked for non-nfsy filesystem, but the current
        #       best idea for it is to check
        #           subprocess.call([
        #               'stat', '--file-system', '--format=%T', tmp_path
        #       ])
        #       to not be nfs. This is only valid for Linux and we'd like to
        #       stay at least also OSX compatible
        tmp_path = '/tmp/spack/tf'
        mkdirp(tmp_path)
        env.set('TEST_TMPDIR', tmp_path)
        env.set('HOME', tmp_path)

    def configure(self, spec, prefix):
        # NOTE: configure script is interactive. If you set the appropriate
        # environment variables, this interactivity is skipped. If you don't,
        # Spack hangs during the configure phase. Use `spack build-env` to
        # determine which environment variables must be set for a particular
        # version.
        configure()

    @run_after('configure')
    def post_configure_fixes(self):
        spec = self.spec
        if self.spec.satisfies('@1.5.0:'):
            # env variable is somehow ignored -> brute force
            # TODO: find a better solution
            filter_file(r'if workspace_has_any_android_rule\(\)',
                        r'if True',
                        'configure.py')

        # version dependent fixes
        if self.spec.satisfies('@1.3.0:1.5.0'):
            # checksum for protobuf that bazel downloads (@github) changed
            filter_file(r'sha256 = "6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93"',
                        r'sha256 = "e5fdeee6b28cf6c38d61243adff06628baa434a22b5ebb7432d2a7fbabbdb13d"',
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
            # https://github.com/tensorflow/tensorflow/issues/20677#issuecomment-404634519
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
            # https://github.com/tensorflow/tensorflow/issues/22395#issuecomment-431229451
            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --distinct_host_configuration=false\n'
                        'build --action_env PYTHONPATH="{0}"'.format(
                            env['PYTHONPATH']),
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
            filter_file(
                r'^build --action_env NCCL_INSTALL_PATH=.*',
                r'build --action_env NCCL_INSTALL_PATH="' +
                spec['nccl'].prefix.lib + '"',
                '.tf_configure.bazelrc')
            filter_file(
                r'^build --action_env NCCL_HDR_PATH=.*',
                r'build --action_env NCCL_HDR_PATH="' +
                spec['nccl'].prefix.include + '"',
                '.tf_configure.bazelrc')

        if self.spec.satisfies('+cuda'):
            libs = [
                spec['cuda'].prefix.lib,
                spec['cuda'].prefix.lib64,
                spec['cudnn'].prefix.lib,
                spec['cudnn'].prefix.lib64,
                spec['nccl'].prefix.lib,
                spec['nccl'].prefix.lib64
            ]
            slibs = ':'.join(libs)

            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --action_env LD_LIBRARY_PATH="' + slibs + '"',
                        '.tf_configure.bazelrc')

    def build(self, spec, prefix):
        if '+cuda' in spec:
            # TODO also consider the case '+gcp'
            # TODO make '--cxxopt...CXX11_ABI=0' a variant
            # For an explanation for ABI build option,
            # see https://www.tensorflow.org/install/source#bazel_build_options
            # Recently noticed that TF_NEED_AWS etc environment variables
            # aren't recognized by configure.py anymore.
            # So, explicitly disable them via bazel options.
            if self.spec.satisfies('@2.1.0-rc0'):
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',
                      '--config=cuda', '--config=noaws', '--config=nogcp',
                      '--config=nohdfs',
                      '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',
                      '--define=tensorflow_mkldnn_contraction_kernel=0',
                      '//tensorflow/tools/pip_package:build_pip_package')
            else:
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',
                      '--config=cuda', '--config=noaws', '--config=nogcp',
                      '--config=nohdfs', '--config=noignite',
                      '--config=nokafka',
                      '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',
                      '//tensorflow/tools/pip_package:build_pip_package')
        else:
            if self.spec.satisfies('@2.1.0-rc0'):
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',
                      '--config=noaws', '--config=nogcp', '--config=nohdfs',
                      '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',
                      '--define=tensorflow_mkldnn_contraction_kernel=0',
                      '//tensorflow/tools/pip_package:build_pip_package')
            else:
                bazel('build', '--jobs={0}'.format(make_jobs), '-c', 'opt',
                      '--config=noaws', '--config=nogcp', '--config=nohdfs',
                      '--config=noignite', '--config=nokafka',
                      '--cxxopt=-D_GLIBCXX_USE_CXX11_ABI=0',
                      '//tensorflow/tools/pip_package:build_pip_package')

        build_pip_package = Executable(
            'bazel-bin/tensorflow/tools/pip_package/build_pip_package')
        tmp_path = env['TEST_TMPDIR']
        build_pip_package(tmp_path)

    def install(self, spec, prefix):
        # using setup.py for installation
        # webpage suggests:
        # sudo pip install /tmp/tensorflow_pkg/tensorflow-0.XYZ.whl
        mkdirp('_python_build')
        cd('_python_build')
        ln = which('ln')

        for fn in glob(join_path(
                "../bazel-bin/tensorflow/tools/pip_package",
                "build_pip_package.runfiles/org_tensorflow/*")):
            ln('-s', fn, '.')
        for fn in glob("../tensorflow/tools/pip_package/*"):
            ln('-s', fn, '.')
        setup_py('install', '--prefix={0}'.format(prefix))

    # TODO: add unit tests
