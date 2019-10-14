# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import environ as env
from spack import *


class Ace(Package):
    """ACE is an open-source framework that provides many components and
       patterns for developing high-performance, distributed real-time and
       embedded systems. ACE provides powerful, yet efficient abstractions
       for sockets, demultiplexing loops, threads, synchronization
       primitives."""

    homepage = "http://www.dre.vanderbilt.edu/~schmidt/ACE.html"
    url = "http://download.dre.vanderbilt.edu/previous_versions/" \
          "ACE-6.5.1.tar.gz"

    version('6.5.6', '6e633602bc04b9d5c20899acdd41d5be0d5c3e53')
    version('6.5.1', '721e0f830930f7bb2ffff9746b2a3fddc4656d71')
    version('6.5.0', 'fee283b02e63e56dd917c1a897283a0a276387c2')

    def install(self, spec, prefix):

        # Dictionary mapping: compiler-name : ACE config-label
        supported = {'intel': '_icc', 'gcc': ''}

        if not(self.compiler.name in supported):
            raise Exception('compiler ' + self.compiler.name +
                            ' not supported in ace spack-package')

        env['ACE_ROOT'] = self.stage.source_path

        with working_dir('./ace'):
            with open('config.h', 'w') as f:
                f.write('#include "ace/config-linux.h"\n')

        with working_dir(join_path(self.stage.source_path,
                                   'include/makeinclude')):
            with open('platform_macros.GNU', 'w') as f:
                f.write("include $(ACE_ROOT)/include/makeinclude/"
                        "platform_linux" + supported[self.compiler.name]
                        + ".GNU\n")
                f.write("INSTALL_PREFIX=%s" % prefix)

        make()
        make('install')
