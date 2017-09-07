##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from distutils.dir_util import copy_tree
from os.path import join
from fnmatch import fnmatch
import os


class Kaldi(Package):    # Does not use Autotools
    """Kaldi is a toolkit for speech recognition written
    in C++ and licensed under the Apache License v2.0.
    Kaldi is intended for use by speech recognition researchers."""

    homepage = "https://github.com/kaldi-asr/kaldi"
    url      = "https://github.com/kaldi-asr/kaldi/archive/master.zip"

    version('master', git='https://github.com/kaldi-asr/kaldi.git')
    version('c024e8', git='https://github.com/kaldi-asr/kaldi.git',
            commit='c024e8aa0a727bf76c91a318f76a1f8b0b59249e')

    variant('shared', default=True,
            description='build shared libraries')
    variant('double', default=False,
            description='build with double precision floats')
    variant('cuda', default=False,
            description='build with CUDA')

    depends_on('blas')
    depends_on('cuda', when='+cuda')
    depends_on('sph2pipe', type='run')
    depends_on('sctk', type='run')
    depends_on('speex', type='run')
    depends_on('openfst@1.4.1-patch', when='@c024e8')
    depends_on('openfst')

    patch('openfst-1.4.1.patch', when='@c024e8')

    def install(self, spec, prefix):
        configure_args = ['--fst-root=' + spec['openfst'].prefix]

        if spec.satisfies('c024e8'):
            configure_args.append('--speex-root=' + spec['speex'].prefix)
            configure_args.append('--fst-version=' +
                                  str(spec['openfst'].version))

        if '~shared' in spec:
            configure_args.append('--static')
        else:
            configure_args.append('--shared')

        if '^openblas' in spec:
            configure_args.append('--mathlib=OPENBLAS')
            configure_args.append('--openblas-root=' + spec['blas'].prefix)
            if '+openmp' in spec['blas'].variants:
                configure_args.append('--threaded-math=yes')
        elif '^atlas' in spec:
            configure_args.append('--mathlib=ATLAS')
            configure_args.append('--atlas-root=' + spec['blas'].prefix)
            if '+pthread' in spec['blas'].variants:
                configure_args.append('--threaded-atlas')
        elif '^intel-parallel-studio' in spec or '^intel-mkl' in spec:
            configure_args.append('--mathlib=MKL')
            configure_args.append('--mkl-root=' + spec['blas'].prefix)
            if '+openmp' in spec['blas'].variants:
                configure_args.append('--mkl-threading=iomp')

        if '+cuda' in spec:
            configure_args.append('--use-cuda=yes')
            configure_args.append('--cudatk-dir=' + spec['cuda'].prefix)

        with working_dir("src"):
            configure(*configure_args)
            make()

            mkdirp(prefix.bin)
            for root, dirs, files in os.walk('bin'):
                for name in files:
                    if os.access(join(root, name), os.X_OK):
                        install(join(root, name), prefix.bin)

            mkdir(prefix.lib)
            copy_tree('lib', prefix.lib)

            for root, dirs, files in os.walk('.'):
                for name in files:
                    if fnmatch(name, '*.h'):
                        mkdirp(join(prefix.include, root.strip("./")))
                        install(join(root, name),
                                join(prefix.include, root.strip("./")))
