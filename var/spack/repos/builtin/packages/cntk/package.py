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
from distutils.dir_util import copy_tree


class Cntk(Package):
    """The Microsoft Cognitive Toolkit is a unified deep-learning toolkit
    that describes neural networks as a series of computational steps
    via a directed graph."""

    homepage = "https://www.microsoft.com/en-us/research/product/cognitive-toolkit"
    url      = "https://github.com/Microsoft/CNTK/archive/v2.0.beta15.0.tar.gz"

    version('master', git='https://github.com/Microsoft/CNTK.git',
            branch='master')
    version('2.0.rc1', 'cdc02a1754cb80999bb7edec3c3ad164')
    version('2.0.beta15.0', '922d9dbc14f0f78774ad48487c918700')

    variant('opencv', default=False, description="Enable OpenCV support.")
    variant('kaldi', default=False, description="Enable Kaldi support.")
    variant('asgd', default=True, description="Enable DataParallelASGD powered by Multiverso.")
    variant('1bitsgd', default=False, description="Enable 1bitsgd support.")
    variant('cuda', default=False, description="Enable CUDA support.")
    variant('debug', default=False, description="Debug build.")

    depends_on('libzip')
    depends_on('openblas')
    depends_on('mpi')
    depends_on('boost')
    depends_on('protobuf@3.1:')
    depends_on('kaldi', when='+kaldi')
    depends_on('opencv', when='+opencv')
    depends_on('cuda', when='+cuda')
    depends_on('cub', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('nccl', when='+cuda')
    depends_on('cntk1bitsgd', when='+1bitsgd')
    depends_on('multiverso@master', when='+asgd')

    def install(self, spec, prefix):
        configure_args = []

        configure_args.append('--with-mpi=' + spec['mpi'].prefix)
        configure_args.append('--with-openblas=' + spec['openblas'].prefix)
        configure_args.append('--with-libzip=' + spec['libzip'].prefix)
        configure_args.append('--with-boost=' + spec['boost'].prefix)
        configure_args.append('--with-protobuf=' + spec['protobuf'].prefix)

        if '+debug' in spec:
            configure_args.append('--with-buildtype=debug')
        else:
            configure_args.append('--with-buildtype=release')

        if '+1bitsgd' in spec:
            configure_args.append('--1bitsgd=yes')

        if '-asgd' in spec:
            configure_args.append('--asgd=no')

        if '+opencv' in spec:
            configure_args.append('--with-opecv=' + spec['opencv'].prefix)

        if '+kaldi' in spec:
            configure_args.append('--with-kaldi=' + spec['kaldi'].prefix)

        if '+cuda' in spec:
            configure_args.append('--cuda=yes')
            configure_args.append('--with-cuda=' + spec['cuda'].prefix)
            configure_args.append('--with-cub=' + spec['cub'].prefix)
            configure_args.append('--with-cudnn=' + spec['cudnn'].prefix)
            configure_args.append('--with-nccl=' + spec['nccl'].prefix)

        configure(*configure_args)

        make()
        mkdirp(prefix.bin)
        copy_tree('bin', prefix.bin)
        mkdirp(prefix.lib)
        copy_tree('lib', prefix.lib)
