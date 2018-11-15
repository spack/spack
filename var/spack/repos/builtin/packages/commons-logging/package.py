# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
