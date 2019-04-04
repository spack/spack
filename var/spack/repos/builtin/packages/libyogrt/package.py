# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libyogrt(AutotoolsPackage):
    """Your One Get Remaining Time Library."""

    homepage = "https://github.com/LLNL/libyogrt"
    url      = "https://github.com/LLNL/libyogrt/releases/download/1.21/libyogrt-1.21.tar.gz"

    version('1.24',   sha256='36695030e72b24b1f22bfcfe42bfd1d3c87f9c0eea5e94ce0120782581ea522f')
    version('1.23',   sha256='c95e7a6be29c0d1ac1b673b0ba1d4e5781981722f93d0da99ae62ff3b5f35b5f')
    version('1.22',   sha256='38e7d1ea3fa030f0169197aa96cde9f01caa595a590764ef1cb2ae07379cb711')
    version('1.21',   sha256='5f8f0942d35ee4e418273e478e632210b3fa648dcb6a2e6a92c6ba4213cdc362')
    version('1.20-7', sha256='735e9d6fa572e239ccc73e11c84b4583338b24df0fa91c48e8bc038d882003f7')
    version('1.20-6', '478f27512842cc5f2b74a0c22b851f60')
    version('1.20-5', 'd0fa6526fcd1f56ddb3d93f602ec72f7')
    version('1.20-4', '092bea10de22c505ce92aa07001decbb')
    version('1.20-3', 'd0507717009a5f8e2009e3b63594738f')
    version('1.20-2', '780bda03268324f6b5f72631fff6e6cb')

    # libyogrt supports the following schedulers:
    #     lcrm, lsf, moab, slurm, AIX+slurm

    # however, only slurm exists in spack
    # libyogrt's build system is smart enough to detect the system scheduler
    # the slurm option here connects to a spack-installed slurm
    # if/when other schedulers have spack packages, they can be added

    variant('scheduler', default='system',
            description="Select scheduler integration",
            values=['system', 'slurm'], multi=False)
    depends_on('slurm', when='scheduler=slurm')

    conflicts('scheduler=lsf', when='@:1.22')

    def url_for_version(self, version):
        if version < Version(1.21):
            return "https://github.com/LLNL/libyogrt/archive/%s.tar.gz" % version
        else:
            return "https://github.com/LLNL/libyogrt/releases/download/{0}/libyogrt-{0}.tar.gz".format(version)

    def configure_args(self):
        args = []

        sched = self.spec.variants['scheduler'].value
        if sched != "system":
            args.append('--with-%s=%s' % (sched, self.spec[sched].prefix))

        return args
