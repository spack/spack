# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAmpltools(PythonPackage):
    """This package includes tools to use with AMPL and amplpy."""

    homepage = "https://ampl.com/"
    pypi = "ampltools/ampltools-0.4.6.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.6",
        sha256="a0c7a21a0492f6809bb866f9887b8ad29b28ce43ea0c2f564562eb883bca34e9",
        url="https://pypi.org/packages/2e/ce/5d7ac093633c8b73e7bfdf34cee14b5dea44e322bf2c938acdfadbb0d735/ampltools-0.4.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests")
