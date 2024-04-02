# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepMl(PythonPackage):
    """Machine Learning for High Energy Physics"""

    homepage = "https://github.com/arogozhnikov/hep_ml"
    pypi = "hep_ml/hep_ml-0.7.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.7.1",
        sha256="9789d015682bf874a610c9410ee5816512b2563985cf5c439a1a73e5d0b15254",
        url="https://pypi.org/packages/aa/d6/9853485fccb5d3cb1b123f731e18509295a22675c926ab5230069abcca73/hep_ml-0.7.1-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="884d133fa5c73793fddd8086914724ab16d6cf8fc4da7a617844e1163ecb557d",
        url="https://pypi.org/packages/f3/d5/c61108b094d29c3a287b2c05834adcfb544b8b1d0cc4eaf144c0c24ac79e/hep_ml-0.7.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.9:", when="@0.4:")
        depends_on("py-pandas@0.14:", when="@0.4:")
        depends_on("py-scikit-learn@0.19.0:", when="@0.6:")
        depends_on("py-scipy@0.15:", when="@0.4:")
        depends_on("py-six", when="@0.4:")
        depends_on("py-theano@1.0.2:", when="@0.6:")
