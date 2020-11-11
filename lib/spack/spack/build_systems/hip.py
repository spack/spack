# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PackageBase
from spack.directives import depends_on, variant, conflicts


class HipPackage(PackageBase):
    """Auxiliary class which contains HIP variant, dependencies and conflicts
    and is meant to unify and facilitate its usage. Closely mimics CudaPackage.

    Maintainers: dtaller
    """

    # https://llvm.org/docs/AMDGPUUsage.html
    # Possible architectures
    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012', 'none'
    )

    variant('hip', default=False, description='Enable HIP support')

    # possible amd gpu targets for hip builds
    variant('amdgpu_target', default='none', values=amdgpu_targets)

    depends_on('llvm-amdgpu', when='+hip')
    depends_on('hsa-rocr-dev', when='+hip')
    depends_on('hip', when='+hip')

    # need amd gpu type for hip builds
    conflicts('amdgpu_target=none', when='+hip')

    # Make sure non-'none' amdgpu_targets cannot be used without +hip
    for value in amdgpu_targets[:-1]:
        conflicts('~hip', when='amdgpu_target=' + value)

    # https://github.com/ROCm-Developer-Tools/HIP/blob/master/bin/hipcc
    # It seems that hip-clang does not (yet?) accept this flag, in which case
    # we will still need to set the HCC_AMDGPU_TARGET environment flag in the
    # hip package file. But I will leave this here for future development.
    @staticmethod
    def hip_flags(amdgpu_target):
        return '--amdgpu-target={0}'.format(amdgpu_target)

    # HIP version vs Architecture

    # TODO: add a bunch of lines like:
    # depends_on('hip@:6.0', when='amdgpu_target=gfx701')
    # to indicate minimum version for each architecture.

    # Compiler conflicts

    # TODO: add conflicts statements along the lines of
    # arch_platform = ' target=x86_64: platform=linux'
    # conflicts('%gcc@5:', when='+cuda ^cuda@:7.5' + arch_platform)
    # conflicts('platform=darwin', when='+cuda ^cuda@11.0.2:')
    # for hip-related limitations.
