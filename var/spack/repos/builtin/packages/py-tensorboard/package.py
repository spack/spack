# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTensorboard(Package):
    """TensorBoard is a suite of web applications for
    inspecting and understanding your TensorFlow runs and
    graphs."""

    homepage = "https://pypi.python.org/project/tensorboard"
    url      = "https://github.com/tensorflow/tensorboard/archive/1.12.2.tar.gz"

    version('2.2.0', sha256='d0dfbf0e4b3b5ebbc3fafa6d281d4b9aa5478eac6bac3330652ab6674278ab77')
    version('1.12.2', sha256='8f1fbf34652e80b66b35b948f2960e98742d38736369997861af781cdc4be3e8')
    depends_on('bazel@0.26.1:', type='build')
    depends_on('py-setuptools', type='build')
    extends('python')

    phases = ['configure', 'build', 'install']

    def setup_build_environment(self, env):
        tmp_path = '/tmp/spack/tb'
        mkdirp(tmp_path)
        env.set('TEST_TMPDIR', tmp_path)

    def configure(self, spec, prefix):
        builddir = join_path(self.stage.source_path, 'spack-build')
        mkdirp(builddir)
        filter_file(r'workdir=.*',
                    'workdir="{0}"'.format(builddir),
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file('trap cleanup EXIT',
                    '',
                    'tensorboard/pip_package/build_pip_package.sh')

    def build(self, spec, prefix):
        tmp_path = env['TEST_TMPDIR']
        bazel('--nohome_rc',
              '--nosystem_rc',
              '--output_user_root=' + tmp_path,
              'build',
              '--verbose_failures',
              '//tensorboard/pip_package')

    def install(self, spec, prefix):
        with working_dir('spack-build'):
            setup_py('install', '--prefix={0}'.format(prefix),
                     '--single-version-externally-managed', '--root=/')
