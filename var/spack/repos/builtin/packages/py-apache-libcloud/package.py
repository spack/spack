# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApacheLibcloud(PythonPackage):
    """Python library for multiple cloud provider APIs"""

    homepage = "https://libcloud.apache.org"
    pypi = "apache-libcloud/apache-libcloud-1.2.1.tar.gz"

    license("Apache-2.0")

    version(
        "1.2.1",
        sha256="6506e51eefe24a0bc0e61699dae7f390e22105e14afc4ba18248748c66117419",
        url="https://pypi.org/packages/2d/32/37c9a6373595e1f335872e0a3ea76420db9c3952e185daff851d209c3b5d/apache_libcloud-1.2.1-py2.py3-none-any.whl",
    )
