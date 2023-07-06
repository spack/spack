# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sheenbidi(MesonPackage):
    """A sophisticated implementation of Unicode Bidirectional Algorithm"""

    homepage = "https://github.com/Tehreer/SheenBidi"
    url = "https://github.com/Tehreer/SheenBidi/archive/v2.6.tar.gz"
    git = "https://github.com/Tehreer/SheenBidi.git"

    version("2.6", sha256="f538f51a7861dd95fb9e3f4ad885f39204b5c670867019b5adb7c4b410c8e0d9")
