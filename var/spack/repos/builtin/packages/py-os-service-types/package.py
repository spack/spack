# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsServiceTypes(PythonPackage):
    """Python library for consuming OpenStack sevice-types-authority data"""

    homepage = "https://docs.openstack.org/os-service-types/"
    pypi = "os-service-types/os-service-types-1.7.0.tar.gz"

    maintainers("haampie")

    version(
        "1.7.0",
        sha256="0505c72205690910077fb72b88f2a1f07533c8d39f2fe75b29583481764965d6",
        url="https://pypi.org/packages/10/2d/318b2b631f68e0fc221ba8f45d163bf810cdb795cf242fe85ad3e5d45639/os_service_types-1.7.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pbr@2:2.0,3:", when="@1:")
