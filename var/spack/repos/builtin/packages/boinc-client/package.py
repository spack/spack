# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BoincClient(AutotoolsPackage):
    """BOINC is a platform for high-throughput computing on a
    large scale (thousands or millions of computers). It can be
    used for volunteer computing (using consumer devices) or
    grid computing (using organizational resources). It
    supports virtualized, parallel, and GPU-based
    applications."""

    homepage = "https://boinc.berkeley.edu/"
    url      = "https://github.com/BOINC/boinc/archive/client_release/7.16/7.16.5.tar.gz"

    version('7.16.16', sha256='0d5656a9f8ed1048936a5764270848b892d63f27bdb863d0ace447f1eaae6002')
    version('7.16.14', sha256='c328399cc27109f94ee77aaf80406ed304c6be6c198391ff8e83f8400431fc78')
    version('7.16.12', sha256='e24dc9c54440dc2032a3b8304f87da5cef12aba3b0889cba6c3761aef8360730')
    version('7.16.11', sha256='8a3f9453b16acfd8c636d18b4939c461c751aa1dd9e108cf60b90a3909bfa0a9')
    version('7.16.10', sha256='adaaa59a8ec4f0658505f6fd319e5abd6651cba15474a8dc25787b1f8d3de30e')
    version('7.16.9',  sha256='0a0cebabe53eb0637328b313d70043e2fd01fe3e896c9b1823dd8db4d90d76e1')
    version('7.16.8',  sha256='826b0b0660167faa48e089bc7aa43120c797436214a3fd99ad32b8b48f85e6d7')
    version('7.16.7',  sha256='38130d532031e75701eee910da64b9eb837e5bfeff9979dbb200c37146be3fed')
    version('7.16.5', sha256='33db60991b253e717c6124cce4750ae7729eaab4e54ec718b9e37f87012d668a')

    variant('manager', default=False, description='Builds the client manager')
    variant('graphics', default=False, description='Graphic apps support')

    # Dependency documentation:
    # https://boinc.berkeley.edu/trac/wiki/SoftwarePrereqsUnix
    conflicts('%gcc@:3.0.4')

    depends_on('autoconf@2.58:', type='build')
    depends_on('automake@1.8:',  type='build')
    depends_on('libtool@1.5:',   type='build')
    depends_on('m4@1.4:',        type='build')

    depends_on('curl@7.17.1:')
    depends_on('openssl@0.9.8:')

    depends_on('freeglut@3:', when='+graphics')
    depends_on('libsm', when='+graphics')
    depends_on('libice', when='+graphics')
    depends_on('libxmu', when='+graphics')
    depends_on('libxi', when='+graphics')
    depends_on('libx11', when='+graphics')
    depends_on('libjpeg', when='+graphics')

    depends_on('wxwidgets@3.0.0:', when='+manager')
    depends_on('libnotify', when='+manager')
    depends_on('sqlite@3.1:', when='+manager')

    patch('systemd-fix.patch')

    def configure_args(self):
        spec = self.spec
        args = []

        args.append("--disable-server")
        args.append("--enable-client")

        if '+manager' in spec:
            args.append('--enable-manager')
        else:
            args.append('--disable-manager')

        return args
