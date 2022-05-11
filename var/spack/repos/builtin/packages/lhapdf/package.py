# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Lhapdf(AutotoolsPackage):
    """LHAPDF is a general purpose C++ interpolator,
       used for evaluating PDFs from discretised data files. """

    homepage = "https://lhapdf.hepforge.org/"
    git      = "https://gitlab.com/hepcedar/lhapdf"
    # the tarballs from hepforge include bundled cython sources
    # that may break the build when using incompatible python versions
    # thus use the release tarball from gitlab that does not include lhapdf.cxx
    url      = "https://gitlab.com/hepcedar/lhapdf/-/archive/lhapdf-6.4.0/lhapdf-lhapdf-6.4.0.tar.gz"

    tags = ['hep']

    version('6.4.0', sha256='155702c36df46de30c5f7fa249193a9a0eea614191de1606301e06cd8062fc29')
    version('6.3.0', sha256='864468439c7662bbceed6c61c7132682ec83381a23c9c9920502fdd7329dd816')
    version('6.2.3', sha256='37200a1ab70247250a141dfed7419d178f9a83bd23a4f8a38e203d4e27b41308')

    variant('python', default=True, description="Build python bindings")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    extends('python', when='+python')
    depends_on('py-cython',     type='build', when='+python')
    depends_on('py-setuptools', type='build', when='+python')

    def configure_args(self):
        args = ['FCFLAGS=-O3', 'CFLAGS=-O3', 'CXXFLAGS=-O3']
        args.extend(self.enable_or_disable('python'))
        return args
