# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNdgHttpsclient(PythonPackage):
    """Provides enhanced HTTPS support for httplib and urllib2 using
    PyOpenSSL."""

    homepage = "https://github.com/cedadev/ndg_httpsclient/"
    pypi = "ndg_httpsclient/ndg_httpsclient-0.5.1.tar.gz"

    version(
        "0.5.1",
        sha256="dd174c11d971b6244a891f7be2b32ca9853d3797a72edb34fa5d7b07d8fff7d4",
        url="https://pypi.org/packages/fb/67/c2f508c00ed2a6911541494504b7cac16fe0b0473912568df65fd1801132/ndg_httpsclient-0.5.1-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="8647bb775de60e79fe795eeee602d705de4500a5b1a3d2224247c217dfa200a9",
        url="https://pypi.org/packages/78/60/1458ed478eb5777498ca57f4fabf2cf9328ac43e5f6db7839cf73704f3a6/ndg_httpsclient-0.5.0-py3-none-any.whl",
    )
