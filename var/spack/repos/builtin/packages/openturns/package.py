# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openturns(CMakePackage):
    """OpenTURNS is an open source initiative for the treatment
    of uncertainties, risks’n statistics in a structured industrial approach.
    """

    homepage = "http://openturns.github.io/openturns/latest/index.html"
    url      = "https://github.com/openturns/openturns/archive/v1.14.tar.gz"

    version('1.14',    sha256='22f55bb3bc6e94a5308d94ad6b6272ea74145ba172746fdc1252a5869eb492a8')
    version('1.13',    sha256='dcdc1b37f7171c4106fa6392cc240ef780198d377938169d3f9ac0e541453930')
    version('1.12.1',  sha256='482388bdd34211b02bf9e9421af58de63be2f7e112e699d2110cd69580011cef')
    version('1.11.1',  sha256='9748b360b412dd16a321375a777ac8b796447b8903e88e000f6bbdd2a5eb99a5')

    variant('hmat', default=False, description='Build with HMat')
    variant('muparser', default=False, description='Build with muparser')
    variant('nlopt', default=False, description='Build with NLopt')
    variant('optpp', default=False, description='Build with OPT++')
    variant('cminpack', default=False, description='Build with CMinpack')
    variant('ceres', default=False, description='Build with Ceres Solver')
    variant('dlib', default=False, description='Build with Dlib')
    variant('boost', default=False, description='Enable Boost support for special functions')
    variant('csv', default=False, description='Build with CSV parser support')
    variant('xml', default=False, description='Build with XML support')
    variant('tbb', default=False, description='Build with multithreading (TBB) support')
    variant('matplotlib', default=False, description='Enable matplotlib for plotting')
    variant('stats', default=False, description='Build with R')
    variant('coupling', default=False, description='Build with coupling support')
    variant('doc', default=False, description='Build the documentation')

    depends_on('pkgconf')
    depends_on('lapack')
    depends_on('blas')
    depends_on('blas')
    depends_on('python')
    depends_on('py-numpy')
    depends_on('py-scipy')
    depends_on('swig')

    depends_on('hmat-oss', when='+hmat')
    depends_on('muparser', when='+muparser')
    depends_on('nlopt+cxx', when='+nlopt')
    depends_on('optpp+blas', when='+optpp')
    depends_on('cminpack+blas', when='+cminpack')
    depends_on('ceres-solver+suitesparse threads=none', when='+ceres')
    depends_on('ceres-solver+suitesparse threads=tbb', when='+ceres+tbb')
    depends_on('dlib threads=none', when='+dlib')
    depends_on('dlib threads=tbb', when='+dlib+tbb')
    depends_on('boost', when='+boost')
    depends_on('flex', when='+csv')
    depends_on('bison', when='+csv')
    depends_on('libxml2', when='+xml')
    depends_on('intel-tbb', when='+tbb')
    depends_on('py-matplotlib', when='+matplotlib')
    depends_on('r', when='+stats')
    depends_on('py-psutil', when='+coupling')
    depends_on('doxygen', when='+doc')
    depends_on('py-sphinx', when='+doc')
    depends_on('py-numpydoc', when='+doc')
    depends_on('py-nbconvert', when='+doc')
    depends_on('py-ipython', when='+doc')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DUSE_BONMIN=OFF',
            '-DUSE_COTIRE=OFF',
            '-DUSE_EXPRTK=OFF',
        ]

        args.extend([
            '-DUSE_BISON:BOOL=%s' % (
                'ON' if '+csv' in spec else 'OFF'),
            '-DUSE_FLEX:BOOL=%s' % (
                'ON' if '+csv' in spec else 'OFF'),
            '-DUSE_BOOST:BOOL=%s' % (
                'ON' if '+boost' in spec else 'OFF'),
            '-DUSE_LIBXML2:BOOL=%s' % (
                'ON' if '+xml' in spec else 'OFF'),
            '-DUSE_TBB:BOOL=%s' % (
                'ON' if '+tbb' in spec else 'OFF'),
            '-DUSE_R:BOOL=%s' % (
                'ON' if '+stats' in spec else 'OFF'),
            '-DUSE_HMAT:BOOL=%s' % (
                'ON' if '+hmat' in spec else 'OFF'),
            '-DUSE_MUPARSER:BOOL=%s' % (
                'ON' if '+muparser' in spec else 'OFF'),
            '-DUSE_NLOPT:BOOL=%s' % (
                'ON' if '+nlopt' in spec else 'OFF'),
            '-DUSE_CERES:BOOL=%s' % (
                'ON' if '+ceres' in spec else 'OFF'),
            '-DUSE_CMINPACK:BOOL=%s' % (
                'ON' if '+cminpack' in spec else 'OFF'),
            '-DUSE_DLIB:BOOL=%s' % (
                'ON' if '+dlib' in spec else 'OFF'),
            '-DUSE_OPTPP:BOOL=%s' % (
                'ON' if '+optpp' in spec else 'OFF'),
        ])

        if '+doc' in spec:
            args.extend([
                '-DUSE_DOXYGEN=ON',
                '-DUSE_SPHINX=ON',
                '-DUSE_NBSPHINX=ON',
            ])
        else:
            args.extend([
                '-DUSE_DOXYGEN=OFF',
                '-DUSE_SPHINX=OFF',
                '-DUSE_NBSPHINX=OFF',
            ])

        return args
