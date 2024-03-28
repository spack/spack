# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoto(PythonPackage):
    """Boto is a Python package that provides interfaces to
    Amazon Web Services."""

    homepage = "https://github.com/boto/boto"
    url = "https://github.com/boto/boto/archive/2.49.0.tar.gz"

    license("MIT")

    version(
        "2.49.0",
        sha256="147758d41ae7240dc989f0039f27da8ca0d53734be0eb869ef16e3adcfa462e8",
        url="https://pypi.org/packages/23/10/c0b78c27298029e4454a472a1919bde20cb182dab1662cec7f2ca1dcc523/boto-2.49.0-py2.py3-none-any.whl",
    )
