# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPem(PythonPackage):
    """
    pem is an MIT-licensed Python module for parsing and splitting of PEM
    files, i.e. Base64 encoded DER keys and certificates.
    """

    homepage = "https://pem.readthedocs.io/en/stable/"
    url = "https://github.com/hynek/pem/archive/20.1.0.tar.gz"

    license("MIT")

    version(
        "20.1.0",
        sha256="aa72dbe04ec2b38435d30b5b233a8be9cb3761947385a622533ba0abd9c21507",
        url="https://pypi.org/packages/93/ba/0bf18feac0688ab6cbb294a31785a51ff8cfd43e34dec9eb97a178dee965/pem-20.1.0-py2.py3-none-any.whl",
    )
    version(
        "19.3.0",
        sha256="ed52902bfee8e7f75c5242538ec4cbab0079cba5cfc7fa260588f5204e12fd9c",
        url="https://pypi.org/packages/61/55/292eed779791d229bbc387bf3225714ebceb6f2197dde24e4057a54a1806/pem-19.3.0-py2.py3-none-any.whl",
    )
    version(
        "19.2.0",
        sha256="3af5c67621b480a26d58654e610d123ef00d7aa5a796ea5cfc7a02b5274347f9",
        url="https://pypi.org/packages/86/aa/1e8d2746a5785b561a6ff10de3e2fe40b49a2d4ba455cbc148ed8ff41cd0/pem-19.2.0-py2.py3-none-any.whl",
    )
    version(
        "19.1.0",
        sha256="f18a51b43de7f3a49c45520975d929eb63bdb0b2e9ec78363d48b852866f3cf8",
        url="https://pypi.org/packages/5b/45/e4b6ecb815c15fc34a33c121934f9242660f0971e15e0c7df8b4f87cbeed/pem-19.1.0-py2.py3-none-any.whl",
    )
    version(
        "18.2.0",
        sha256="471b1fd50d50124bc3435f5b25faf074392f3d02feb1e9c663811f0db2093aca",
        url="https://pypi.org/packages/da/bd/a4afebec48dffcbaa373578926bb6d2fdc073e75355dc96b684a6cd81d42/pem-18.2.0-py2.py3-none-any.whl",
    )
    version(
        "18.1.0",
        sha256="53aab93ebbec110e07274822cdbcd5fcc278fa8fc6e74762027797b8e141365b",
        url="https://pypi.org/packages/6b/ea/772d0bbcfb897e58538a81de6c8b85d818dddf883d7b114c8c0467ec6fff/pem-18.1.0-py2.py3-none-any.whl",
    )
    version(
        "17.1.0",
        sha256="f64f0eb25f700a83cbb21b8f82a1a470f0fd75865e2c84606b3f912b01f65f48",
        url="https://pypi.org/packages/c5/67/334ded5b53377a171b66fcbc0c8b8e90bed1be6cb4334377406cb1c99030/pem-17.1.0-py2.py3-none-any.whl",
    )
    version(
        "16.1.0",
        sha256="6b56282315e2e01dda7be7a0567268cbc8b602491bb408cb0cdd4bdcb7207fe0",
        url="https://pypi.org/packages/47/31/950a775056ffafa5d8a914d98ae767b74c9bc66373546be790e12d76e985/pem-16.1.0-py2.py3-none-any.whl",
    )
    version(
        "16.0.0",
        sha256="2f3046ef3503d325fdc7a8ff111a8364b1279ef882921c3685a45d69690b27b8",
        url="https://pypi.org/packages/39/c0/e052ad47e51ab874ccbea3d65cf9590d840da686a1b5bbc08b512ee4dc0a/pem-16.0.0-py2.py3-none-any.whl",
    )
    version(
        "15.0.0",
        sha256="6c034feee2a79dc646954ff3a33c87fcf731d01a36b4414e0c2aa6694af8c7aa",
        url="https://pypi.org/packages/4a/b5/6646fb5c6dd39d7f438a5579debe8833fe66348a85a00cff7c745e83d9df/pem-15.0.0-py2.py3-none-any.whl",
    )
