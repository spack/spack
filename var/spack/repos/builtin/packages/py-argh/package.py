# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgh(PythonPackage):
    """An argparse wrapper that doesn't make you say "argh" each time
    you deal with it.

    Building a command-line interface? Found yourself uttering "argh!"
    while struggling with the API of argparse? Don't like the complexity
    but need the power? Argh is a smart wrapper for argparse. Argparse is
    a very powerful tool; Argh just makes it easy to use."""

    homepage = "https://github.com/neithere/argh/"
    pypi = "argh/argh-0.26.2.tar.gz"

    maintainers("dorton21")

    version(
        "0.26.2",
        sha256="a9b3aaa1904eeb78e32394cd46c6f37ac0fb4af6dc488daa58971bdc7d7fcaf3",
        url="https://pypi.org/packages/06/1c/e667a7126f0b84aaa1c56844337bf0ac12445d1beb9c8a6199a7314944bf/argh-0.26.2-py2.py3-none-any.whl",
    )
