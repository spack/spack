# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRsa(PythonPackage):
    """Pure-Python RSA implementation"""

    homepage = "https://stuvel.eu/rsa"
    pypi = "rsa/rsa-3.4.2.tar.gz"

    license("Apache-2.0")

    version(
        "4.9",
        sha256="90260d9058e514786967344d0ef75fa8727eed8a7d2e43ce9f4bcf1b536174f7",
        url="https://pypi.org/packages/49/97/fa78e3d2f65c02c8e1268b9aba606569fe97f6c8f7c2d74394553347c145/rsa-4.9-py3-none-any.whl",
    )
    version(
        "4.7.2",
        sha256="78f9a9bf4e7be0c5ded4583326e7461e3a3c5aae24073648b4bdfa797d78c9d2",
        url="https://pypi.org/packages/e9/93/0c0f002031f18b53af7a6166103c02b9c0667be528944137cc954ec921b3/rsa-4.7.2-py3-none-any.whl",
    )
    version(
        "4.0",
        sha256="14ba45700ff1ec9eeb206a2ce76b32814958a98e372006c8fb76ba820211be66",
        url="https://pypi.org/packages/02/e5/38518af393f7c214357079ce67a317307936896e961e35450b70fad2a9cf/rsa-4.0-py2.py3-none-any.whl",
    )
    version(
        "3.4.2",
        sha256="43f682fea81c452c98d09fc316aae12de6d30c4b5c84226642cf8f8fd1c93abd",
        url="https://pypi.org/packages/e1/ae/baedc9cb175552e95f3395c43055a6a5e125ae4d48a1d7a924baca83e92e/rsa-3.4.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@4.1:4.1.0,4.3,4.4.1:4.7.0,4.7.2:")
        depends_on("py-pyasn1@0.1.3:", when="@4.1:4.1.0,4.3:4.7.0,4.7.2:")
