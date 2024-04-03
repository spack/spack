# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUrlNormalize(PythonPackage):
    """URL normalization for Python."""

    homepage = "https://github.com/niksite/url-normalize"
    pypi = "url-normalize/url-normalize-1.4.3.tar.gz"

    license("MIT")

    version(
        "1.4.3",
        sha256="ec3c301f04e5bb676d333a7fa162fa977ad2ca04b7e652bfc9fac4e405728eed",
        url="https://pypi.org/packages/65/1c/6c6f408be78692fc850006a2b6dea37c2b8592892534e09996e401efc74b/url_normalize-1.4.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@1.4.3:")
