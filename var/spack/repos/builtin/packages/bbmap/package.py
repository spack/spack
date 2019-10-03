# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bbmap(Package):
    """Short read aligner for DNA and RNA-seq data."""

    homepage = "http://sourceforge.net/projects/bbmap/"
    url      = "https://downloads.sourceforge.net/project/bbmap/BBMap_38.63.tar.gz"

    version('38.63', sha256='089064104526c8d696164aefa067f935b888bc71ef95527c72a98c17ee90a01f')
    version('37.36', '1e1086e1fae490a7d03c5a065b1c262f')

    depends_on('java')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.set('BBMAP_CONFIG', self.prefix.bin.config)
        run_env.set('BBMAP_RESOURCES', self.prefix.bin.resources)
