# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTldextract(PythonPackage):
    """
    Accurately separates a URL's subdomain, domain, and public suffix,
    using the Public Suffix List (PSL). By default, this includes the
    public ICANN TLDs and their exceptions. You can optionally support
    the Public Suffix List's private domains as well.
    """

    homepage = "https://github.com/john-kurkowski/tldextract"
    pypi = "tldextract/tldextract-3.4.1.tar.gz"

    maintainers("LydDeb")

    license("BSD-3-Clause")

    version(
        "5.1.1",
        sha256="b9c4510a8766d377033b6bace7e9f1f17a891383ced3c5d50c150f181e9e1cc2",
        url="https://pypi.org/packages/d0/de/3f37b2568115c7ebeae39508dc1092f04f3dc286f22ef30171baca9c9cf2/tldextract-5.1.1-py3-none-any.whl",
    )
    version(
        "3.4.1",
        sha256="26f646987b01ae2946e7491cce4aaf54129f3489a196a274e6c843ec72968313",
        url="https://pypi.org/packages/fb/21/dad9eaedad757362458f92f9345307cc847956ab9775ee9ab5a0fcb912cf/tldextract-3.4.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@5:")
        depends_on("python@3.7:", when="@3.2:4")
        depends_on("py-filelock@3.0.8:")
        depends_on("py-idna")
        depends_on("py-requests@2.1:")
        depends_on("py-requests-file@1.4:")
