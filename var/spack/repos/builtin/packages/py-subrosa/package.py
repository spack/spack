# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySubrosa(PythonPackage):
    """Subrosa is a Python implementation of Shamir's Secret Sharing. An
    algorithm for sharing a secret with a group of people without letting any
    individual of the group know the secret."""

    homepage = "https://github.com/DasIch/subrosa/"
    url = "https://github.com/DasIch/subrosa/archive/0.1.0.tar.gz"

    version(
        "0.1.0",
        sha256="f5db667411fddd71a2196da839c289fb0531b3d6d31b7b34492a8b9c01ae5d33",
        url="https://pypi.org/packages/fb/bd/d8d6b96314e564fb4f4ff2701a027aee7442ccc1d28c301588182ac0d329/subrosa-0.1.0-py2.py3-none-any.whl",
    )
