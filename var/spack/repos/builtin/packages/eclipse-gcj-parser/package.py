# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class EclipseGcjParser(Package):
    """GCJ requires the Eclipse Java parser, but does not ship with it.
    This builds that parser into an executable binary, thereby
    making GCJ work."""

    homepage = "https://github.com/spack/spack/issues/8165"
    url = "ftp://sourceware.org/pub/java/ecj-4.8.jar"
    # Official download found at (see ecj-4.8M4.jar and ecjsrc-4.8M4.jar)
    # http://download.eclipse.org/eclipse/downloads/drops4/S-4.8M4-201712062000/

    maintainers = ['citibeth']

    version('4.8', 'd7cd6a27c8801e66cbaa964a039ecfdb', expand=False)

    phases = ('build', 'install')

    @property
    def gcj(self):
        """Obtain Executable for the gcj included with this GCC,
        even in the face of GCC binaries with version numbers
        included in their names."""

        dir, gcc = os.path.split(str(self.compiler.cc))
        if 'gcc' not in gcc:
            raise ValueError(
                'Package {0} requires GCC to build'.format(self.name))

        return Executable(join_path(dir, gcc.replace('gcc', 'gcj')))

    def build(self, spec, prefix):
        self.gcj(
            '-o', 'ecj1',
            '--main=org.eclipse.jdt.internal.compiler.batch.GCCMain',
            'ecj-4.8.jar')

    def install(self, spec, prefix):
        mkdirp(spec.prefix.bin)
        install('ecj1', spec.prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.bin)
