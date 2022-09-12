# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libraqm(MesonPackage):
    """Raqm is a small library that encapsulates the logic for complex text layout and provides a convenient API."""

    homepage = "https://github.com/HOST-Oman/libraqm"
    url      = "https://github.com/HOST-Oman/libraqm/releases/download/v0.9.0/raqm-0.9.0.tar.xz"
    git      = "https://github.com/HOST-Oman/libraqm.git"

    version('0.9.0', tag="v0.9.0")

    depends_on("freetype")
    depends_on("harfbuzz")
