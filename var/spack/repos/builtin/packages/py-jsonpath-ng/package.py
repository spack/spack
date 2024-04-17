# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsonpathNg(PythonPackage):
    """A final implementation of JSONPath for Python that aims to be
    standard compliant, including arithmetic and binary comparison
    operators."""

    homepage = "https://github.com/h2non/jsonpath-ng"
    pypi = "jsonpath-ng/jsonpath-ng-1.5.2.tar.gz"

    license("Apache-2.0")

    version(
        "1.6.0",
        sha256="6fd04833412c4b3d9299edf369542f5e67095ca84efa17cbb7f06a34958adc9f",
        url="https://pypi.org/packages/92/8d/f6592a8267fcf85d4066605d671b509b456866b962554112c562d2b8be4b/jsonpath_ng-1.6.0-py3-none-any.whl",
    )
    version(
        "1.5.3",
        sha256="292a93569d74029ba75ac2dc3d3630fc0e17b2df26119a165fa1d498ca47bf65",
        url="https://pypi.org/packages/4c/b7/3627068d9aa6b2d49af117eb3897770a5dbc6bb3f4c09ed56a9eb749438e/jsonpath_ng-1.5.3-py3-none-any.whl",
    )
    version(
        "1.5.2",
        sha256="93d1f248be68e485eb6635c3a01b2d681f296dc349d71e37c8755837b8944d36",
        url="https://pypi.org/packages/ae/03/a8a12e49e88ba7983d704ef518e25041206aa2e934686270516f1bc439ff/jsonpath_ng-1.5.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-decorator", when="@1.5")
        depends_on("py-ply", when="@1.5:")
        depends_on("py-six", when="@1.5")
