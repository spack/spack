# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FdFind(CargoPackage):
    """A simple, fast and user-friendly alternative to 'find'."""

    homepage = "https://github.com/sharkdp/fd"

    crates_io = "fd-find"
    git = "https://github.com/sharkdp/fd.git"

    version('master', branch='master')
    version('8.0.0', sha256='c2c514a6aab9cfbfc920668f39bb745e4ac24545408ab817aa8a4554f639e635')
    version('7.5.0', sha256='111941422349755e27f9c7c443e0043e9fe31384cd503b133fb27a2b04c78fbc')
    version('7.4.0', sha256='b21777867eb06d903a152fcc45e774e319b0d49ab3ab9d30cf1a38f7c541f590')