# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DependsOnGitversion(Package):
    homepage = "example.com"
    url = "fake.com"

    version("main", branch="main")
    version("0.0.0", sha256="0123456789abcdef0123456789abcdef")

    depends_on("develop-branch-version@git.foo=0.2.15")
