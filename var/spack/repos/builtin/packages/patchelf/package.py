# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Patchelf(AutotoolsPackage):
    """PatchELF is a small utility to modify the dynamic linker and RPATH of
       ELF executables."""

    homepage = "https://nixos.org/patchelf.html"
    url      = "https://nixos.org/releases/patchelf/patchelf-0.10/patchelf-0.10.tar.bz2"
    list_url = "https://nixos.org/releases/patchelf/"
    list_depth = 1

    version('0.10', sha256='f670cd462ac7161588c28f45349bc20fb9bd842805e3f71387a320e7a9ddfcf3')
    version('0.9',  sha256='a0f65c1ba148890e9f2f7823f4bedf7ecad5417772f64f994004f59a39014f83')
    version('0.8',  sha256='c99f84d124347340c36707089ec8f70530abd56e7827c54d506eb4cc097a17e7')
