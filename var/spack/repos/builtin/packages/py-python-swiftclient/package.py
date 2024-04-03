# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSwiftclient(PythonPackage):
    """This is a python client for the Swift API."""

    homepage = "https://docs.openstack.org/python-swiftclient"
    pypi = "python-swiftclient/python-swiftclient-3.9.0.tar.gz"

    maintainers("ajkotobi")

    version(
        "3.12.0",
        sha256="07c63cf223127b7047e034c71532c71277d95ad60ba1d38bbae5bed2f4342c09",
        url="https://pypi.org/packages/7b/71/454f3d6c72b9a7740295afed58e4382c06bd9a8b2657f98dad3ab9ec521f/python_swiftclient-3.12.0-py2.py3-none-any.whl",
    )
    version(
        "3.11.1",
        sha256="eb53bf614eb276896002884c9cf5c2bbdff56da49e9e343df088d180baf8c685",
        url="https://pypi.org/packages/49/e5/692e4383986f5b5893d495961d8582501679082b51ab139ca8153abff07d/python_swiftclient-3.11.1-py2.py3-none-any.whl",
    )
    version(
        "3.10.0",
        sha256="fc504de50fa1c37b4869c9badd1bd2161bf212475ecbad954abd8327b224a383",
        url="https://pypi.org/packages/3e/b7/b3d61ef72cfa37083f67dcd440d009b05bfbcc350791de61d4fd220a205c/python_swiftclient-3.10.0-py2.py3-none-any.whl",
    )
    version(
        "3.9.0",
        sha256="cba38ac00a69bcea610318bfbe4f8aaee9d7b46705359477b8d3602ea2009878",
        url="https://pypi.org/packages/cb/a5/f901ca2b74aa8ad1eb051407b2cdb09f311d02a3f3ba77a4c27629d052be/python_swiftclient-3.9.0-py2.py3-none-any.whl",
    )
    version(
        "3.8.1",
        sha256="0b460f6a2c16d474dd2a85674162a04e14f40a21d9ef0197172fb5c5cc0bc5d5",
        url="https://pypi.org/packages/1a/6c/1dca59a10d9689203599b1507f0420242cfe914fa518063f5cebf36207b1/python_swiftclient-3.8.1-py2.py3-none-any.whl",
    )
    version(
        "3.8.0",
        sha256="9d8c76cc78dbf252f9c6f57e5a5f45299fceb06ac13c04de431a73610110ff89",
        url="https://pypi.org/packages/1d/00/4461030f0b0937475029c959dc21d254c02d6809e6102a12287ec2d4843b/python_swiftclient-3.8.0-py2.py3-none-any.whl",
    )
    version(
        "3.7.1",
        sha256="179449354b9dcda6f24c5f66826d8a59263c531761d0ce83591ea4aedbd656d4",
        url="https://pypi.org/packages/91/9e/bec42f5bf9dbe31417888b76a0c68e85ba07505e1b4775655c1b70745b55/python_swiftclient-3.7.1-py2.py3-none-any.whl",
    )

    variant("keystone", default=False, description="Enable keystone authentication")

    with default_args(type="run"):
        depends_on("py-python-keystoneclient@0.7:", when="+keystone")
        depends_on("py-requests@1.1:", when="@:3")
        depends_on("py-six@1.9:", when="@3.6:3")
