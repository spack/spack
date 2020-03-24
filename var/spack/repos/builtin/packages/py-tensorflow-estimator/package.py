# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorflowEstimator(Package):
    """TensorFlow Estimator is a high-level TensorFlow API that greatly
    simplifies machine learning programming."""

    homepage = "https://github.com/tensorflow/estimator"
    url      = "https://github.com/tensorflow/estimator/archive/v1.13.0.tar.gz"

    version('2.0.0', sha256='6f4bdf1ab219e1f1cba25d2af097dc820f56479f12a839853d97422fe4d8b465')
    version('1.13.0', sha256='a787b150ff436636df723e507019c72a5d6486cfe506886279d380166953f12f', preferred=True)

    extends('python')

    depends_on('py-tensorflow@2.0.0',  when='@2.0.0')
    depends_on('py-tensorflow@1.13.1', when='@1.13.0')

    depends_on('bazel@0.19.0', type='build')
    depends_on('py-pip', type='build')
    depends_on('py-funcsigs@1.0.2:', type=('build', 'run'))

    def install(self, spec, prefix):
        tmp_path = join_path(env.get('SPACK_TMPDIR', '/tmp/spack'),
                             'tf-estimator',
                             self.module.site_packages_dir[1:])
        mkdirp(tmp_path)
        env['TEST_TMPDIR'] = tmp_path
        env['HOME'] = tmp_path

        # bazel uses system PYTHONPATH instead of spack paths
        bazel('--action_env', 'PYTHONPATH={0}'.format(env['PYTHONPATH']),
              '//tensorflow_estimator/tools/pip_package:build_pip_package')

        build_pip_package = Executable(join_path(
            'bazel-bin/tensorflow_estimator/tools',
            'pip_package/build_pip_package'))
        build_pip_package(tmp_path)

        pip = Executable('pip')
        pip('install', '--prefix={0}'.format(prefix),
            '--find-links={0}'.format(tmp_path), 'tensorflow-estimator')
