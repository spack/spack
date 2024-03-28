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
        sha256="d2c7225f6a1c6cf698af4ebc962da70178a99bcde24ee6d1961c4f3338130d57",
        url="https://pypi.org/packages/bf/b2/26470fde7ff55169df8e071fb42cb1f83e22bd952520ab2b5c5a5edc2acd/ndg_httpsclient-0.5.1-py2-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="683b7a17e8b093e422562e8b089a3ad5d87e00f8f8765aac128791ab9140eef3",
        url="https://pypi.org/packages/4b/a1/73ba15c5e56be36f184b0eabf7ea0873ea54022238313757e55781e8a2ad/ndg_httpsclient-0.5.0-py2-none-any.whl",
    )
