# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxMultiversion(PythonPackage):
    """A Sphinx extension for building self-hosted versioned documentation."""

    homepage = "https://github.com/Holzhaus/sphinx-multiversion"
    pypi = "sphinx-multiversion/sphinx-multiversion-0.2.4.tar.gz"

    version(
        "0.2.4",
        sha256="dec29f2a5890ad68157a790112edc0eb63140e70f9df0a363743c6258fbeb478",
        url="https://pypi.org/packages/05/ad/4989e6be165805694e93d09bc57425aa1368273b7de4fe3083fe4310803a/sphinx_multiversion-0.2.4-py3-none-any.whl",
    )
    version(
        "0.2.3",
        sha256="dc0f18449122e3e2a61245771bfdb7fa83df4f6adbf8eafea31f5b0cfccb5dbe",
        url="https://pypi.org/packages/a1/c3/b3f0ed867ff11fce503f180e03e1cb6bee41567f5928842af919b0b8e280/sphinx_multiversion-0.2.3-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="02ca21264b7995ddcba46d2d03e6f97c34989af262316b41c3ed99f9e0ba3649",
        url="https://pypi.org/packages/c0/1e/7eadbb1ff882954212e931f54ef24fa7f38fb07ac35480be1f17ac8d420d/sphinx_multiversion-0.2.2-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="5c3ba8fc3687126733dbe9d458120fff5d59f41b09621671271879f7549649c9",
        url="https://pypi.org/packages/51/17/f1733bf0ad5ba97b6c3884f2219f7321e405e3a3843c07b43686062c33e3/sphinx_multiversion-0.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-sphinx@2.1:")
