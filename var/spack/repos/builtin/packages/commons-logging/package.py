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


class CommonsLogging(Package):
    """When writing a library it is very useful to log information. However
    there are many logging implementations out there, and a library cannot
    impose the use of a particular one on the overall application that the
    library is a part of.

    The Logging package is an ultra-thin bridge between different logging
    implementations. A library that uses the commons-logging API can be used
    with any logging implementation at runtime. Commons-logging comes with
    support for a number of popular logging implementations, and writing
    adapters for others is a reasonably simple task."""

    homepage = "http://commons.apache.org/proper/commons-logging/"
    url      = "http://archive.apache.org/dist/commons/logging/binaries/commons-logging-1.2-bin.tar.gz"

    version('1.2',   'ac043ce7ab3374eb4ed58354a6b2c3de')
    version('1.1.3', 'b132f9a1e875677ae6b449406cff2a78')
    version('1.1.1', 'e5de09672af9b386c30a311654d8541a')

    extends('jdk')
    depends_on('java', type='run')

    def install(self, spec, prefix):
        install('commons-logging-{0}.jar'.format(self.version), prefix)
