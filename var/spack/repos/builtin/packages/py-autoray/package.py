# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAutoray(PythonPackage):
    """Write backend agnostic numeric code compatible with any numpy-ish array library."""

    homepage = "https://github.com/jcmgray/autoray"
    pypi = "autoray/autoray-0.5.3.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.3",
        sha256="84ccca6f095445559540cc2b2dd25cf258d204ee7608cdc958f49c56b5ae20a2",
        url="https://pypi.org/packages/60/66/628602262963edbd8e8997cb0082022e7064b8f2585315423a899c437edf/autoray-0.5.3-py3-none-any.whl",
    )
