# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Yaksa(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Yaksa is a high-performance datatype engine for expressing,
    managing and manipulating data present in noncontiguous memory
    regions. It provides portable abstractions for structured
    noncontiguous data layouts that are much more comprehensive compared
    with traditional I/O vectors.

    Yaksa imitates parts of the MPI Datatype system, but adds additional
    functionality that would allow it to be used independent of MPI. It
    provides routines for packing/unpacking, creating I/O vectors (array
    of contiguous segments) and flattening/unflattening datatypes into
    process-portable formats.

    Yaksa's backend includes support for CPUs as well as different
    GPUs."""

    homepage = "https://www.yaksa.org"
    url      = "https://github.com/pmodels/yaksa/archive/refs/tags/v0.2.tar.gz"
    maintainers = ['raffenet', 'yfguo', 'hzhou']

    version('0.2', sha256='9401cb6153dc8c34ddb9781bbabd418fd26b0a27b5da3294ecc21af7be9c86f2')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('python@3:', type='build')
    depends_on('hip', when='+rocm')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('autogen.sh')

    def configure_args(self):
        spec = self.spec
        config_args = []
        config_args += self.with_or_without('cuda', activation_value='prefix')

        if '+rocm' in spec:
            config_args.append('--with-hip={0}'.format(spec['hip'].prefix))
            rocm_archs = spec.variants['amdgpu_target'].value
            if 'none' not in rocm_archs:
                config_args.append('--with-hip-sm={0}'.format(",".join(rocm_archs)))
        else:
            config_args.append('--without-hip')

        return config_args
