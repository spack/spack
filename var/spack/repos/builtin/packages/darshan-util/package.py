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


class DarshanUtil(Package):
    """Darshan (util) is collection of tools for parsing and summarizing log
    files produced by Darshan (runtime) instrumentation. This package is
    typically installed on systems (front-end) where you intend to analyze
    log files produced by Darshan (runtime)."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"

    version('3.1.0', '439d717323e6265b2612ed127886ae52')
    version('3.0.0', '732577fe94238936268d74d7d74ebd08')

    depends_on('zlib')

    def install(self, spec, prefix):

        options = ['CC=%s' % self.compiler.cc,
                   '--with-zlib=%s' % spec['zlib'].prefix]

        with working_dir('spack-build', create=True):
            configure = Executable('../darshan-util/configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('install')
