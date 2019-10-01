# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob


class Bowtie2(Package):
    """Bowtie 2 is an ultrafast and memory-efficient tool for aligning
       sequencing reads to long reference sequences"""

    homepage = "bowtie-bio.sourceforge.net/bowtie2/index.shtml"
    url      = "http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.3.1/bowtie2-2.3.1-source.zip"

    version('2.3.5.1', sha256='335c8dafb1487a4a9228ef922fbce4fffba3ce8bc211e2d7085aac092155a53f')
    version('2.3.5', sha256='2b6b2c46fbb5565ba6206b47d07ece8754b295714522149d92acebefef08347b')
    version('2.3.4.1', '8371bbb6eb02ae99c5cf633054265cb9')
    version('2.3.1', 'b4efa22612e98e0c23de3d2c9f2f2478')
    version('2.3.0', '3ab33f30f00f3c30fec1355b4e569ea2')
    version('2.2.5', '51fa97a862d248d7ee660efc1147c75f')

    depends_on('tbb', when='@2.3.0:')
    depends_on('readline', when='@2.3.1:')
    depends_on('perl', type='run')
    depends_on('python', type='run')
    depends_on('zlib', when='@2.3.1:')

    patch('bowtie2-2.2.5.patch', when='@2.2.5', level=0)
    patch('bowtie2-2.3.1.patch', when='@2.3.1', level=0)
    patch('bowtie2-2.3.0.patch', when='@2.3.0', level=0)
    resource(name='simde', git="https://github.com/nemequ/simde",
             destination='.', when='target=aarch64:')

    # seems to have trouble with 6's -std=gnu++14
    conflicts('%gcc@6:', when='@:2.3.1')
    conflicts('@:2.3.5.0', when='target=aarch64:')

    def patch(self):
        if self.spec.target.family == 'aarch64':
            copy_tree('simde', 'third_party/simde')
            if self.spec.satisfies('%gcc@:4.8.9'):
                filter_file('-fopenmp-simd', '', 'Makefile')

    @run_before('install')
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
           can fix up the path to the perl|python binary.
        """

        with working_dir(self.stage.source_path):
            kwargs = {'ignore_absent': True, 'backup': False, 'string': False}

            match = '^#!/usr/bin/env perl'
            perl = self.spec['perl'].command
            substitute = "#!{perl}".format(perl=perl)
            files = ['bowtie2', ]
            filter_file(match, substitute, *files, **kwargs)

            match = '^#!/usr/bin/env python'
            python = self.spec['python'].command
            substitute = "#!{python}".format(python=python)
            files = ['bowtie2-build', 'bowtie2-inspect']
            filter_file(match, substitute, *files, **kwargs)

    def install(self, spec, prefix):
        make_arg = []
        if self.spec.target.family == 'aarch64':
            make_arg.append('POPCNT_CAPABILITY=0')
        make(*make_arg)
        mkdirp(prefix.bin)
        for bow in glob("bowtie2*"):
            install(bow, prefix.bin)
        # install('bowtie2',prefix.bin)
        # install('bowtie2-align-l',prefix.bin)
        # install('bowtie2-align-s',prefix.bin)
        # install('bowtie2-build',prefix.bin)
        # install('bowtie2-build-l',prefix.bin)
        # install('bowtie2-build-s',prefix.bin)
        # install('bowtie2-inspect',prefix.bin)
        # install('bowtie2-inspect-l',prefix.bin)
        # install('bowtie2-inspect-s',prefix.bin)
