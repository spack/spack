# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class SonamesNotDetectable(Package):
    """Package that declares the libraries it owns, but cannot be detected"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/sonames-not-detectable-1.0.tar.gz"

    sonames = [r"^libsonames-owner\.so\.\d+$"]

    version("1.0", md5="0123456789abcdef0123456789abcdef")
