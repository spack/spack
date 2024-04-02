# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeystoneauth1(PythonPackage):
    """
    This package contains tools for authenticating to an OpenStack-based
    cloud
    """

    homepage = "https://docs.openstack.org/keystoneauth/"
    pypi = "keystoneauth1/keystoneauth1-4.3.1.tar.gz"

    maintainers("haampie")

    version(
        "4.3.1",
        sha256="c4a80b79bc3e0412eb127fa761e80912614f8563646ca34b62bcd9d533f93077",
        url="https://pypi.org/packages/7a/1b/8c5d1fd19b9e08d3a3b64492d078039c7ddd166c3cf029154f1c5f0439f7/keystoneauth1-4.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-iso8601@0.1.11:")
        depends_on("py-os-service-types@1.2:")
        depends_on("py-pbr@2:2.0,3:")
        depends_on("py-requests@2.14.2:")
        depends_on("py-six@1.10:", when="@:5.1")
        depends_on("py-stevedore@1.20:")
