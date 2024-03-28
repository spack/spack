# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyProgressbar2(PythonPackage):
    """A progress bar for Python 2 and Python 3"""

    homepage = "https://github.com/WoLpH/python-progressbar"
    pypi = "progressbar2/progressbar2-3.50.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.55.0",
        sha256="e98fee031da31ab9138fd8dd838ac80eafba82764eb75a43d25e3ca622f47d14",
        url="https://pypi.org/packages/ed/19/afcfa7b88021a172f4f5308ca3cd95709c6ac39787caa720576e4b6cf6ba/progressbar2-3.55.0-py2.py3-none-any.whl",
    )
    version(
        "3.50.1",
        sha256="7849b84c01a39e4eddd2b369a129fed5e24dfb78d484ae63f9e08e58277a2928",
        url="https://pypi.org/packages/3d/b6/c76b09749f889bd53ca9aa1a4ec1dc990ff6d004cf079b43f5022ee37855/progressbar2-3.50.1-py2.py3-none-any.whl",
    )
    version(
        "3.43.1",
        sha256="39a987c263401d94e687869562c0943e6f9bfaa3215aebda180dfa935be72e38",
        url="https://pypi.org/packages/a3/72/1e88c46edd372d46f989db9b0168951b080a83666b6820bb8159a3d62280/progressbar2-3.43.1-py2.py3-none-any.whl",
    )
    version(
        "3.39.3",
        sha256="1ea89e2aaa1da85450aabbd2af62cefa04f1ee1c567f3a11ee0d8ded14fd1fea",
        url="https://pypi.org/packages/fb/89/d90f9ff03285d8eb56994e8cec1b73a4d0dc9bb529c1f8e8e10b1b663843/progressbar2-3.39.3-py2.py3-none-any.whl",
    )
