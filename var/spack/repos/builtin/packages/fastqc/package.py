# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fastqc(Package):
    """A quality control tool for high throughput sequence data."""

    homepage = "http://www.bioinformatics.babraham.ac.uk/projects/fastqc/"
    url = "http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip"

    version('0.11.7', '8fead05fa62c5e723f0d2157a9b5fcd4')
    version('0.11.5', '3524f101c0ab0bae77c7595983170a76')
    version('0.11.4', '104ff2e0e9aebf5bee1f6b068a059b0d')

    depends_on('java', type='run')
    depends_on('perl')          # for fastqc "script", any perl will do

    patch('fastqc.patch', level=0)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.lib)
        install('fastqc', prefix.bin)
        for j in ['cisd-jhdf5.jar', 'jbzip2-0.9.jar', 'sam-1.103.jar']:
            install(j, prefix.lib)
        for d in ['Configuration', 'net', 'org', 'Templates', 'uk']:
            install_tree(d, join_path(prefix.lib, d))
        chmod = which('chmod')
        chmod('+x', prefix.bin.fastqc)

    # In theory the 'run' dependency on 'jdk' above should take
    # care of this for me. In practice, it does not.
    def setup_environment(self, spack_env, run_env):
        """Add <prefix> to the path; the package has a script at the
           top level.
        """
        run_env.prepend_path('PATH', self.spec['java'].prefix.bin)
