# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Wxwidgets(AutotoolsPackage):
    """wxWidgets is a C++ library that lets developers create
       applications for Windows, Mac OS X, Linux and other platforms
       with a single code base. It has popular language bindings for
       Python, Perl, Ruby and many other languages, and unlike other
       cross-platform toolkits, wxWidgets gives applications a truly
       native look and feel because it uses the platform's native API
       rather than emulating the GUI. It's also extensive, free,
       open-source and mature."""

    homepage = "http://www.wxwidgets.org/"
    url      = "https://github.com/wxWidgets/wxWidgets/releases/download/v3.1.0/wxWidgets-3.1.0.tar.bz2"
    git      = "https://github.com/wxWidgets/wxWidgets.git"

    version('develop', branch='master')
    version('3.1.0', '2170839cfa9d9322e8ee8368b21a15a2497b4f11')
    version('3.0.2', '6461eab4428c0a8b9e41781b8787510484dea800')
    version('3.0.1', '73e58521d6871c9f4d1e7974c6e3a81629fddcf8')

    patch('math_include.patch', when='@3.0.1:3.0.2')

    depends_on('pkgconfig', type='build')
    depends_on('gtkplus')

    @when('@:3.0.2')
    def build(self, spec, prefix):
        make(parallel=False)

    def configure_args(self):
        spec = self.spec
        options = [
            '--enable-unicode',
            '--disable-precomp-headers'
        ]

        # see http://trac.wxwidgets.org/ticket/17639
        if spec.satisfies('@:3.1.0') and sys.platform == 'darwin':
            options.extend([
                '--disable-qtkit',
                '--disable-mediactrl'
            ])

        return options
