# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyShellescape(PythonPackage):
    """Shell escape a string to safely use it as a token in a shell command"""

    homepage = "https://github.com/chrissimpkins/shellescape"
    pypi = "shellescape/shellescape-3.8.1.tar.gz"

    version(
        "3.8.1",
        sha256="f17127e390fa3f9aaa80c69c16ea73615fd9b5318fd8309c1dca6168ae7d85bf",
        url="https://pypi.org/packages/d0/f4/0081137fceff5779cd4205c1e96657e41cc2d2d56c940dc8eeb6111780f7/shellescape-3.8.1-py2.py3-none-any.whl",
    )
