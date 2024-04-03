# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperlink(PythonPackage):
    """A featureful, immutable, and correct URL for Python."""

    homepage = "https://github.com/python-hyper/hyperlink"
    pypi = "hyperlink/hyperlink-21.0.0.tar.gz"

    license("MIT")

    version(
        "21.0.0",
        sha256="e6b14c37ecb73e89c77d78cdb4c2cc8f3fb59a885c5b3f819ff4ed80f25af1b4",
        url="https://pypi.org/packages/6e/aa/8caf6a0a3e62863cbb9dab27135660acba46903b703e224f14f447e57934/hyperlink-21.0.0-py2.py3-none-any.whl",
    )
