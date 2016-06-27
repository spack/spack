##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

class Stat(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    homepage = "http://paradyn.org/STAT/STAT.html"
    url      = "https://github.com/lee218llnl/stat/archive/v2.0.0.tar.gz"

    version('2.2.0', '26bd69dd57a15afdd5d0ebdb0b7fb6fc')
    version('2.1.0', 'ece26beaf057aa9134d62adcdda1ba91')
    version('2.0.0', 'c7494210b0ba26b577171b92838e1a9b')

    variant('dysect', default=False, description="enable DySectAPI")

    depends_on('libelf')
    depends_on('libdwarf')
    depends_on('dyninst')
    depends_on('graphlib')
    depends_on('graphviz')
    depends_on('launchmon')
    depends_on('mrnet')

    patch('configure_mpicxx.patch', when='@2.1.0')

    def install(self, spec, prefix):
        configure_args = [
            "--enable-gui",
            "--prefix=%s" % prefix,
            "--disable-examples", # Examples require MPI: avoid this dependency.
            "--with-launchmon=%s"   % spec['launchmon'].prefix,
            "--with-mrnet=%s"       % spec['mrnet'].prefix,
            "--with-graphlib=%s"    % spec['graphlib'].prefix,
            "--with-stackwalker=%s" % spec['dyninst'].prefix,
            "--with-libdwarf=%s"    % spec['libdwarf'].prefix
            ]
        if '+dysect' in spec:
            configure_args.append('--enable-dysectapi')
        configure(*configure_args)

        make(parallel=False)
        make("install")
