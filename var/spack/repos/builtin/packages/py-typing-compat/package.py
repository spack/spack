# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypingCompat(PythonPackage):
    """Python typing compatibility library."""

    homepage = "https://github.com/rossmacarthur/typing-compat"
    git = "https://github.com/rossmacarthur/typing-compat.git"
    pypi = "typing-compat/typing-compat-0.1.0.tar.gz"

    version("0.1.0", sha256="a7159db80406de342bc128ab315fae3afe1ddc87cbc2df7a023763090fdfe5d2")

    depends_on("py-setuptools", type="build")
