# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Canu(MakefilePackage):
    """A single molecule sequence assembler for genomes large and
       small."""

    homepage = "http://canu.readthedocs.io/"
    url      = "https://github.com/marbl/canu/archive/v1.5.tar.gz"

    version('1.7.1', sha256='c314659c929ee05fd413274f391463a93f19b8337eabb7ee5de1ecfc061caafa')
    version('1.5', '65df275baa28ecf11b15dfd7343361e3')

    depends_on('gnuplot', type='run')
    depends_on('jdk', type='run')
    depends_on('perl', type='run')

    build_directory = 'src'

    def patch(self):
        # Use our perl, not whatever is in the environment
        filter_file(r'^#!/usr/bin/env perl',
                    '#!{0}'.format(self.spec['perl'].command.path),
                    'src/pipelines/canu.pl')

    def install(self, spec, prefix):
        # replicate the Makefile logic here:
        # https://github.com/marbl/canu/blob/master/src/Makefile#L344
        uname = which('uname')
        ostype = uname(output=str).strip()
        machinetype = uname('-m', output=str).strip()
        if machinetype == 'x86_64':
            machinetype = 'amd64'
        target_dir = '{0}-{1}'.format(ostype, machinetype)
        bin = join_path(target_dir, 'bin')

        install_tree(bin, prefix.bin)
