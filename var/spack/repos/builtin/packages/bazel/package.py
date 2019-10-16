# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack import *
from multiprocessing import cpu_count
from spack.util.environment import env_flag
from spack.build_environment import SPACK_NO_PARALLEL_MAKE


class Bazel(Package):
    """Bazel is Google's own build tool"""

    homepage = "https://www.bazel.io"
    url = "https://github.com/bazelbuild/bazel/releases/download/0.11.1/bazel-0.11.1-dist.zip"

    version('0.17.2', sha256='b6e87acfa0a405bb8b3417c58477b66d5bc27dc0d31ba6fa12bc255b9278d33b')
    version('0.16.1', sha256='09c66b94356c82c52f212af52a81ac28eb06de1313755a2f23eeef84d167b36c')
    version('0.15.0', sha256='c3b716e6625e6b8c323350c95cd3ae0f56aeb00458dddd10544d5bead8a7b602')
    version('0.14.1', sha256='d49cdcd82618ae7a7a190e6f0a80d9bf85c1a66b732f994f37732dc14ffb0025')
    version('0.13.0', sha256='82e9035084660b9c683187618a29aa896f8b05b5f16ae4be42a80b5e5b6a7690')
    version('0.12.0', sha256='3b3e7dc76d145046fdc78db7cac9a82bc8939d3b291e53a7ce85315feb827754')
    version('0.11.1', sha256='e8d762bcc01566fa50952c8028e95cfbe7545a39b8ceb3a0d0d6df33b25b333f')
    version('0.11.0', sha256='abfeccc94728cb46be8dbb3507a23ccffbacef9fbda96a977ef4ea8d6ab0d384')
    version('0.10.1', sha256='708248f6d92f2f4d6342006c520f22dffa2f8adb0a9dc06a058e3effe7fee667')
    version('0.10.0', sha256='47e0798caaac4df499bce5fe554a914abd884a855a27085a4473de1d737d9548')
    version('0.9.0', sha256='efb28fed4ffcfaee653e0657f6500fc4cbac61e32104f4208da385676e76312a')
    version('0.4.5', sha256='2b737be42678900470ae9e48c975ac5b2296d9ae23c007bf118350dbe7c0552b')
    version('0.4.4', sha256='d52a21dda271ae645711ce99c70cf44c5d3a809138e656bbff00998827548ebb')

    depends_on('java@8:', type=('build', 'link', 'run'))
    depends_on('zip')

    patch('fix_env_handling.patch', when='@:0.4.5')
    patch('fix_env_handling-0.9.0.patch', when='@0.9.0:0.12.0')
    patch('fix_env_handling-0.13.0.patch', when='@0.13.0:0.13.999')
    patch('fix_env_handling-0.17.2.patch', when='@0.14.0:')
    patch('link.patch')
    patch('cc_configure.patch', when='@:0.4.5')
    patch('unix_cc_configure.patch', when='@0.9.0')
    patch('unix_cc_configure-0.10.0.patch', when='@0.10.0:0.14.999')
    patch('unix_cc_configure-0.17.2.patch', when='@0.15.0:')

    def url_for_version(self, version):
        if version >= Version('0.4.1'):
            return 'https://github.com/bazelbuild/bazel/releases/download/{0}/bazel-{0}-dist.zip'.format(version)
        else:
            return 'https://github.com/bazelbuild/bazel/archive/{0}.tar.gz'.format(version)

    def install(self, spec, prefix):
        bash = which('bash')
        bash('-c', './compile.sh')
        mkdir(prefix.bin)
        install('output/bazel', prefix.bin)

    def setup_dependent_package(self, module, dependent_spec):
        class BazelExecutable(Executable):
            """Special callable executable object for bazel so the user can
               specify parallel or not on a per-invocation basis.  Using
               'parallel' as a kwarg will override whatever the package's
               global setting is, so you can either default to true or false
               and override particular calls.

               Note that if the SPACK_NO_PARALLEL_MAKE env var is set it
               overrides everything.
            """

            def __init__(self, name, command, jobs):
                super(BazelExecutable, self).__init__(name)
                self.bazel_command = command
                self.jobs = jobs

            def __call__(self, *args, **kwargs):
                disable = env_flag(SPACK_NO_PARALLEL_MAKE)
                parallel = ((not disable) and kwargs.get('parallel',
                                                         self.jobs > 1))

                jobs = "--jobs=1"
                if parallel:
                    jobs = "--jobs=%d" % self.jobs

                args = (self.bazel_command,) + (jobs,) + args

                return super(BazelExecutable, self).__call__(*args, **kwargs)

        jobs = cpu_count()
        dependent_module = inspect.getmodule(dependent_spec.package)
        if not dependent_spec.package.parallel:
            jobs = 1
        elif dependent_module.make_jobs:
            jobs = dependent_module.make_jobs
        module.bazel = BazelExecutable('bazel', 'build', jobs)
