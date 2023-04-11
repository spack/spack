# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lsof(AutotoolsPackage):
    """Lsof displays information about files open to Unix processes."""

    homepage = "https://lsof.readthedocs.io/"
    url = "https://github.com/lsof-org/lsof/releases/download/4.98.0/lsof-4.98.0.tar.gz"
    git = "https://github.com/lsof-org/lsof.git"

    maintainers("jiegec")

    version("4.98.0", sha256="2f8efa62cdf8715348b8f76bf32abf59f109a1441df35c686d23dccdeed34d99")
