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
from multiprocessing import cpu_count
from spack.util.environment import env_flag
from spack.build_environment import SPACK_NO_PARALLEL_MAKE


class Bazel(Package):
    """Bazel is Google's own build tool"""

    homepage = "https://www.bazel.io"
    url = "https://github.com/bazelbuild/bazel/archive/0.3.1.tar.gz"

    version('0.4.4', '5e7c52b89071efc41277e2f0057d258f',
            url="https://github.com/bazelbuild/bazel/releases/download/0.4.4/bazel-0.4.4-dist.zip")
    version('0.3.1', '5c959467484a7fc7dd2e5e4a1e8e866b')
    version('0.3.0', '33a2cb457d28e1bee9282134769b9283')
    version('0.2.3', '393a491d690e43caaba88005efe6da91')
    version('0.2.2b', '75081804f073cbd194da1a07b16cba5f')
    version('0.2.2', '644bc4ea7f429d835e74f255dc1054e6')

    depends_on('jdk@8:')
    patch('fix_env_handling.patch')
    patch('link.patch')
    patch('cc_configure.patch')

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
                parallel = ((not disable) and
                            kwargs.get('parallel', self.jobs > 1))

                jobs = "--jobs=1"
                if parallel:
                    jobs = "--jobs=%d" % self.jobs

                args = (self.bazel_command,) + (jobs,) + args

                return super(BazelExecutable, self).__call__(*args, **kwargs)

        jobs = cpu_count()
        if not dependent_spec.package.parallel:
            jobs = 1
        elif dependent_spec.package.make_jobs:
            jobs = dependent_spec.package.make_jobs
        module.bazel = BazelExecutable('bazel', 'build', jobs)
