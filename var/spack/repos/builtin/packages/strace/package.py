# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Strace(AutotoolsPackage):
    """Strace is a diagnostic, debugging and instructional userspace
    utility for Linux. It is used to monitor and tamper with interactions
    between processes and the Linux kernel, which include system calls,
    signal deliveries, and changes of process state."""

    homepage = "https://strace.io"
    url      = "https://github.com/strace/strace/releases/download/v5.2/strace-5.2.tar.xz"

    conflicts('platform=darwin', msg='strace runs only on Linux.')

    version('5.2', sha256='d513bc085609a9afd64faf2ce71deb95b96faf46cd7bc86048bc655e4e4c24d2')
    version('5.1', sha256='f5a341b97d7da88ee3760626872a4899bf23cf8dee56901f114be5b1837a9a8b')
    version('5.0', sha256='3b7ad77eb2b81dc6078046a9cc56eed5242b67b63748e7fc28f7c2daf4e647da')
    version('4.21', sha256='5c7688db44073e94c59a5627744e5699454419824cc8166e8bcfd7ec58375c37')

    def configure_args(self):
        args = []
        if self.spec.target.family == 'aarch64':
            args.append('--enable-mpers=no')
        else:
            args.append('--enable-mpers=yes')
        return args
