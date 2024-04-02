# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLooseversion(PythonPackage):
    """Version numbering for anarchists and software realists."""

    homepage = "https://github.com/effigies/looseversion"
    pypi = "looseversion/looseversion-1.0.2.tar.gz"

    version(
        "1.2.0",
        sha256="0b30eaca26506135c1109dbed582384f8503dee8fcfe07b85fd949f69f077977",
        url="https://pypi.org/packages/76/26/25bbdec19a4351425db4ff319882243e01984c593ce88a1da67b6489e2b0/looseversion-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="e38414e8e3f4a636084cecb910dc1ab88980289a06b1e5c57948b83becc7861c",
        url="https://pypi.org/packages/41/70/466273a3876394309e5890477a6fc51b83ed8624cc28b627de72a262d258/looseversion-1.0.2-py3-none-any.whl",
    )
