# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jackcess(Package):
    """Jackcess is a pure Java library for reading from and writing to
    MS Access databases (currently supporting versions 2000-2016)."""

    homepage = "http://jackcess.sourceforge.net/"
    url      = "https://sourceforge.net/projects/jackcess/files/jackcess/2.1.12/jackcess-2.1.12.jar"

    version('2.1.12',   '7d051d8dd93f2fe7e5e86389ea380619', expand=False)
    version('1.2.14.3', 'ef778421c1385ac9ab4aa7edfb954caa', expand=False,
            url='https://sourceforge.net/projects/jackcess/files/jackcess/Older%20Releases/1.2.14.3/jackcess-1.2.14.3.jar')

    extends('jdk')
    depends_on('java', type='run')
    depends_on('commons-lang@2.6', when='@2.1.12', type='run')
    depends_on('commons-lang@2.4', when='@1.2.14.3', type='run')
    depends_on('commons-logging@1.1.3', when='@2.1.12', type='run')
    depends_on('commons-logging@1.1.1', when='@1.2.14.3', type='run')

    def install(self, spec, prefix):
        install('jackcess-{0}.jar'.format(self.version), prefix)
