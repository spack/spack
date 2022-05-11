# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyTensorflowHub(Package):
    """TensorFlow Hub is a library to foster the publication, discovery, and
    consumption of reusable parts of machine learning models."""

    homepage = "https://github.com/tensorflow/hub"
    url = "https://github.com/tensorflow/hub/archive/refs/tags/v0.12.0.tar.gz"

    maintainers = ['aweits']

    version('0.12.0', sha256='b192ef3a9a6cbeaee46142d64b47b979828dbf41fc56d48c6587e08f6b596446')
    version('0.11.0', sha256='4715a4212b45531a7c25ada7207d850467d1b5480f1940f16623f8770ad64df4')

    extends('python')

    depends_on('bazel', type='build')
    depends_on('py-pip', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('python@3.6:',        type=('build', 'run'))
    depends_on('py-numpy@1.12.0:',   type=('build', 'run'))
    depends_on('py-protobuf@3.8.0:',   type=('build', 'run'))

    def install(self, spec, prefix):
        tmp_path = tempfile.mkdtemp(prefix='spack')
        env['TEST_TMPDIR'] = tmp_path
        env['HOME'] = tmp_path
        args = [
            # Don't allow user or system .bazelrc to override build settings
            '--nohome_rc',
            '--nosystem_rc',
            # Bazel does not work properly on NFS, switch to /tmp
            '--output_user_root=' + tmp_path,
            'build',
            # Spack logs don't handle colored output well
            '--color=no',
            '--jobs={0}'.format(make_jobs),
            # Enable verbose output for failures
            '--verbose_failures',
            # Show (formatted) subcommands being executed
            '--subcommands=pretty_print',
            '--spawn_strategy=local',
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            '--explain=explainlogfile.txt',
            # Increase verbosity of explanation,
            '--verbose_explanations',
            # bazel uses system PYTHONPATH instead of spack paths
            '--action_env', 'PYTHONPATH={0}'.format(env['PYTHONPATH']),
            '//tensorflow_hub/pip_package:build_pip_package',
        ]

        bazel(*args)

        runfiles = join_path('bazel-bin', 'tensorflow_hub', 'pip_package',
                             'build_pip_package.runfiles', 'org_tensorflow_hub')
        insttmp_path = tempfile.mkdtemp(prefix='spack')
        install(join_path('tensorflow_hub', 'pip_package', 'setup.py'),  insttmp_path)
        install(join_path('tensorflow_hub', 'pip_package', 'setup.cfg'), insttmp_path)
        install('LICENSE', join_path(insttmp_path, 'LICENSE.txt'))
        mkdirp(join_path(insttmp_path, 'tensorflow_hub'))
        install_tree(join_path(runfiles, 'tensorflow_hub'),
                     join_path(insttmp_path, 'tensorflow_hub'))

        with working_dir(insttmp_path):
            args = std_pip_args + ['--prefix=' + prefix, '.']
            pip(*args)

        remove_linked_tree(tmp_path)
        remove_linked_tree(insttmp_path)
