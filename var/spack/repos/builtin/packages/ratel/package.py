# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ratel(MakefilePackage, CudaPackage, ROCmPackage):
    """Extensible, performance-portable solid mechanics with libCEED and PETSc"""

    homepage = "https://ratel.micromorph.org"
    git = "https://gitlab.com/micromorph/ratel.git"

    maintainers = ['jedbrown', 'jeremylt']

    version('develop', branch='main')
    version('0.1.2', tag='v0.1.2')

    # development version
    depends_on('libceed@develop', when='@develop')
    depends_on('petsc@main', when='@develop')

    # version 0.1.2
    depends_on('libceed@0.10.1:0.10', when='@0.1.2')
    depends_on('petsc@3.17:3.17', when='@0.1.2')

    # Note: '+cuda' and 'cuda_arch' variants are added by the CudaPackage
    #       '+rocm' and 'amdgpu_target' variants are added by the ROCmPackage
    # But we need to sync cuda/rocm with libCEED and PETSc
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on('libceed+cuda cuda_arch={0}'.format(sm_),
                   when='+cuda cuda_arch={0}'.format(sm_))
        depends_on('petsc+cuda cuda_arch={0}'.format(sm_),
                   when='+cuda cuda_arch={0}'.format(sm_))
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on('libceed+rocm amdgpu_target={0}'.format(gfx),
                   when='+rocm amdgpu_target={0}'.format(gfx))
        depends_on('petsc+rocm amdgpu_target={0}'.format(gfx),
                   when='+rocm amdgpu_target={0}'.format(gfx))
    # Kokkos required for AMD GPUs
    depends_on('petsc+kokkos', when='+rocm')

    def configure(self, spec, prefix):
        options = [
            'CEED_DIR=%s' % spec['libceed'].prefix,
            'PETSC_DIR=%s' % spec['petsc'].prefix,
        ]
        make('configure', *options)

    def edit(self, spec, prefix):
        make('info', *sef.common_make_opts)

    @property
    def build_targets(self, spec, prefix):
        return self.common_make_opts

    @property
    def install_targets(self, spec, prefix):
        return ['prefix={0}'.format(self.prefix)] + self.common_make_opts

    def check(self):
        make('prove', *self.common_make_opts, parallel=False)
