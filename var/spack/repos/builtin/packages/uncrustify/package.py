# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Uncrustify(Package):
    """Source Code Beautifier for C, C++, C#, ObjectiveC, Java, and others."""

    homepage = "http://uncrustify.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/uncrustify/uncrustify/uncrustify-0.61/uncrustify-0.61.tar.gz"

    version('0.67', '0c9a08366e5c97cd02ae766064e957de41827611')
    version('0.61', 'b6140106e74c64e831d0b1c4b6cf7727')

    depends_on('cmake', type='build', when='@0.64:')

    @when('@0.64:')
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make('install')

    @when('@:0.62')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(self.prefix))
        make()
        make('install')
