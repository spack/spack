##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Libmonitor(AutotoolsPackage):
    """Libmonitor is a library providing callback functions for the
    begin and end of processes and threads.  It provides a layer on
    which to build process monitoring tools and profilers."""

    homepage = "https://github.com/HPCToolkit/libmonitor"
    git      = "https://github.com/HPCToolkit/libmonitor.git"

    version('master', branch='master')
    version('2018.07.18', commit='d28cc1d3c08c02013a68a022a57a6ac73db88166',
            preferred=True)
    version('2013.02.18', commit='4f2311e413fd90583263d6f20453bbe552ccfef3')

    # Configure for Rice HPCToolkit.
    variant('hpctoolkit', default=False,
            description='Configure for HPCToolkit')

    variant('bgq', default=False,
            description='Configure for Blue Gene/Q')

    # Configure for Krell and OpenSpeedshop.
    variant('krellpatch', default=False,
            description="Build with openspeedshop based patch.")

    patch('libmonitorkrell-0000.patch', when='@2013.02.18+krellpatch')
    patch('libmonitorkrell-0001.patch', when='@2013.02.18+krellpatch')
    patch('libmonitorkrell-0002.patch', when='@2013.02.18+krellpatch')

    signals = 'SIGBUS, SIGSEGV, SIGPROF, 36, 37, 38'

    # Set default cflags (-g -O2) and move to the configure line.
    def flag_handler(self, name, flags):
        if name != 'cflags':
            return (flags, None, None)

        if '-g' not in flags:
            flags.append('-g')
        for flag in flags:
            if flag.startswith('-O'):
                break
        else:
            flags.append('-O2')

        return (None, None, flags)

    def configure_args(self):
        args = []

        if '+hpctoolkit' in self.spec:
            args.append('--enable-client-signals=%s' % self.signals)

        # TODO: Spack has trouble finding cross-compilers; the +bgq variant
        # manually specifies the appropriate compiler to build for BGQ (by
        # setting that here, Spack's choice of CC is overridden).
        # If the user manually defines an entry in compilers.yaml, the bgq
        # variant should not be required if the user specifies the bgq
        # architecture for the libmonitor package. See #8860
        # TODO: users want to build this for the backend and dependents for the
        # frontend. Spack ought to make that easy by finding the appropriate
        # compiler for each if the root and libmonitor are designated to build
        # on the frontend and backend, respectively. As of now though, there
        # is an issue with compiler concretization such that spack will attempt
        # to assign the compiler chosen for libmonitor to the root (unless the
        # user specifies the compiler for each in addition to the arch).
        # See #8859
        if '+bgq' in self.spec:
            args.append('CC=powerpc64-bgq-linux-gcc')

        return args
