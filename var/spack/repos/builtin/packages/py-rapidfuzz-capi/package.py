# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRapidfuzzCapi(PythonPackage):
    """
    C-API of RapidFuzz, which can be used to extend RapidFuzz from separate packages.
    """

    homepage = "https://github.com/maxbachmann/rapidfuzz_capi"
    pypi = "rapidfuzz_capi/rapidfuzz_capi-1.0.5.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "1.0.5",
        sha256="c557114d1f30adbb6918973b9e46fd3923d957f6f734079bd90881095e0e1252",
        url="https://pypi.org/packages/ea/ff/76d9cf0a7566d34c520cb6632ad856bd71cffef4c28d99728cc3b59545fc/rapidfuzz_capi-1.0.5-py3-none-any.whl",
    )
