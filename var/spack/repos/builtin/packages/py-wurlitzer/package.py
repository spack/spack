# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWurlitzer(PythonPackage):
    """Capture C-level stdout/stderr pipes in Python via os.dup2."""

    pypi = "wurlitzer/wurlitzer-3.0.2.tar.gz"

    maintainers("sethrj")

    license("MIT")

    version(
        "3.0.2",
        sha256="37f3ed1b08bf887172eda7f5177417241ec54cdd5e70df74c92d96875ceff632",
        url="https://pypi.org/packages/d3/16/4ed932c896808eae84ad92ea62dcfd5c8433b36fdd00dfc38b213abde178/wurlitzer-3.0.2-py3-none-any.whl",
    )
