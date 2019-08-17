# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hsakmt(AutotoolsPackage):
    """hsakmt is a thunk library that provides a userspace interface to amdkfd
    (AMD's HSA Linux kernel driver). It is the HSA equivalent of libdrm."""

    homepage = "https://cgit.freedesktop.org/amd/hsakmt/"
    url      = "https://www.x.org/archive/individual/lib/hsakmt-1.0.0.tar.gz"

    version('1.0.0', '9beb20104e505300daf541266c4c3c3d')
