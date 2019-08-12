# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "https://strace.io/files/4.21/strace-4.21.tar.xz"

    conflicts('platform=darwin', msg='strace runs only on Linux.')

    version('5.0', sha256='3b7ad77eb2b81dc6078046a9cc56eed5242b67b63748e7fc28f7c2daf4e647da')
    version('4.21', '785b679a75e9758ebeb66816f315b9fe')
