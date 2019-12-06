# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Quantlib(AutotoolsPackage):
    """A free/open-source library for quantitative finance."""

    homepage = "http://quantlib.org"
    url      = "https://bintray.com/quantlib/releases/download_file?file_path=QuantLib-1.16.tar.gz"

    maintainers = ['TheQueasle']

    version('1.16', '1e7298cedcf74afdf8244391a2d9a99b')

    depends_on('boost')
    depends_on('bash')

    variant('examples', default=True, description="""
        If enabled, examples are built and installed when "make" and "make
        install" are invoked. If disabled they are built but not installed.
        """)
    variant('intraday', default=True, description="""
        If enabled, date objects will support an intraday
        datetime resolution down to microseconds. Strickly
        monotone daycounters (Actual360, Actual365Fixed and
        ActualActual) will take the additional information
        into account and allow for accurate intraday
        pricing. If disabled (the default) the smallest
        resolution of date objects will be a single day.
        Intraday datetime resolution is experimental.
        """)
    variant('openmp', default=True, description="""
        If enabled, configure will try to detect and enable OpenMP support.
        """)
    variant('static', default=True, description="Build static libraries")
    variant('shared', default=True, description="Build shared libraries")
    variant('std-classes', default=True, description="""
        This is a shortcut for
        --enable-std-pointers --enable-std-unique-ptr --enable-std-function. If
        enabled, this supersedes any --disable option passed
        """)

    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()

    def configure_args(self):
        spec = self.spec
        args = []

        args.append('--with-boost-include'.format(
            spec['boost'].prefix.include))
        args.append('--with-boost-lib'.format(spec['boost'].prefix.lib))

        if '+intraday' in spec:
            args.append('--enable-intraday')
        else:
            args.append('--disable-intraday')

        if '+openmp' in spec:
            args.append('--enable-openmp')
        else:
            args.append('--disable-openmp')

        if '+static' in spec:
            args.append('--enable-static')
        else:
            args.append('--disable-static')

        if '+shared' in spec:
            args.append('--enable-shared')
        else:
            args.append('--disable-shared')

        if '+examples' in spec:
            args.append('--enable-examples')
        else:
            args.append('--disable-examples')

        if '+std-classes' in spec:
            args.append('--enable-std-classes')
        else:
            args.append('--disable-std-classes')

        return args
