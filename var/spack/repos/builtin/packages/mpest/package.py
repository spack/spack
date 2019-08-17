# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpest(MakefilePackage):
    """MP-EST estimates species trees from a set of gene trees by maximizing
       a pseudo-likelihood function."""

    homepage = "http://faculty.franklin.uga.edu/lliu/content/mp-est"
    url      = "https://faculty.franklin.uga.edu/lliu/sites/faculty.franklin.uga.edu.lliu/files/mpest_1.5.zip"

    version('1.5', 'f176d5301aa26567918664e5e30027d1')

    @property
    def build_directory(self):
        return join_path('mpest_{0}'.format(self.version), 'src')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install('mpest', prefix.bin)

    def setup_environment(self, spack_env, run_env):
        if self.spec.satisfies('platform=darwin'):
            spack_env.set('ARCHITECTURE', 'mac')
        else:
            spack_env.set('ARCHITECTURE', 'unix')
