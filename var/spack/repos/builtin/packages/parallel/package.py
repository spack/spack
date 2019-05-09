# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Parallel(AutotoolsPackage):
    """GNU parallel is a shell tool for executing jobs in parallel using
    one or more computers. A job can be a single command or a small
    script that has to be run for each of the lines in the input.
    """

    homepage = "http://www.gnu.org/software/parallel/"
    url      = "https://ftpmirror.gnu.org/parallel/parallel-20170122.tar.bz2"

    version('20190222', sha256='86b1badc56ee2de1483107c2adf634604fd72789c91f65e40138d21425906b1c')
    version('20170322', '4fe1b8d2e3974d26c77f0b514988214d')
    version('20170122', 'c9f0ec01463dc75dbbf292fd8be5f1eb')
    version('20160422', '24621f684130472694333709bd4454cb')
    version('20160322', '4e81e0d36902ab4c4e969ee6f35e6e57')

    def check(self):
        # The Makefile has a 'test' target, but it does not work
        make('check')

    depends_on('perl', type=('build', 'run'))

    @run_before('install')
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
           can fix up the path to the perl binary.
        """
        perl = self.spec['perl'].command
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

        with working_dir('src'):
            match = '^#!/usr/bin/env perl|^#!/usr/bin/perl.*'
            substitute = "#!{perl}".format(perl=perl)
            files = ['parallel', 'niceload', 'parcat', 'sql', ]
            filter_file(match, substitute, *files, **kwargs)
