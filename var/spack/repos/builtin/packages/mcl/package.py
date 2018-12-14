# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mcl(AutotoolsPackage):
    """The MCL algorithm is short for the Markov Cluster Algorithm, a fast
       and scalable unsupervised cluster algorithm for graphs (also known
       as networks) based on simulation of (stochastic) flow in graphs."""

    homepage = "https://www.micans.org/mcl/index.html"
    url      = "https://www.micans.org/mcl/src/mcl-14-137.tar.gz"

    version('14-137', 'bc8740456cf51019d0a9ac5eba665bb5')

    depends_on('perl')

    def configure_args(self):
        return ['--enable-blast']

    @run_after('install')
    def filter_sbang(self):
        with working_dir(prefix.bin):
            substitute = "#!{perl}".format(perl=self.spec['perl'].command.path)
            kwargs = {'ignore_absent': True, 'backup': False, 'string': False}
            filter_file('^#!/usr/bin/env perl', substitute, 'mclpipeline', **kwargs)
            filter_file('^#!/usr/local/bin/perl -w', substitute, 'mcxdeblast', **kwargs)
