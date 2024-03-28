# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCertifi(PythonPackage):
    """Certifi: A carefully curated collection of Root Certificates for validating
    the trustworthiness of SSL certificates while verifying the identity of TLS
    hosts."""

    homepage = "https://github.com/certifi/python-certifi"
    pypi = "certifi/certifi-2020.6.20.tar.gz"

    license("MPL-2.0")

    version(
        "2023.7.22",
        sha256="92d6037539857d8206b8f6ae472e8b77db8058fec5937a1ef3f54304089edbb9",
        url="https://pypi.org/packages/4c/dd/2234eab22353ffc7d94e8d13177aaa050113286e93e7b40eae01fbf7c3d9/certifi-2023.7.22-py3-none-any.whl",
    )
    version(
        "2023.5.7",
        sha256="c6c2e98f5c7869efca1f8916fed228dd91539f9f1b444c314c06eef02980c716",
        url="https://pypi.org/packages/9d/19/59961b522e6757f0c9097e4493fa906031b95b3ebe9360b2c3083561a6b4/certifi-2023.5.7-py3-none-any.whl",
    )
    version(
        "2022.12.7",
        sha256="4ad3232f5e926d6718ec31cfc1fcadfde020920e278684144551c91769c7bc18",
        url="https://pypi.org/packages/71/4c/3db2b8021bd6f2f0ceb0e088d6b2d49147671f25832fb17970e9b583d742/certifi-2022.12.7-py3-none-any.whl",
    )
    version(
        "2022.9.14",
        sha256="e232343de1ab72c2aa521b625c80f699e356830fd0e2c620b465b304b17b0516",
        url="https://pypi.org/packages/6a/34/cd29f4dd8a23ce45f2b8ce9631ff2d4205fb74eddb412a3dc4fd1e4aa800/certifi-2022.9.14-py3-none-any.whl",
    )
    version(
        "2021.10.8",
        sha256="d62a0163eb4c2344ac042ab2bdf75399a71a2d8c7d47eac2e2ee91b9d6339569",
        url="https://pypi.org/packages/37/45/946c02767aabb873146011e665728b680884cd8fe70dde973c640e45b775/certifi-2021.10.8-py2.py3-none-any.whl",
    )
    version(
        "2020.6.20",
        sha256="8fc0819f1f30ba15bdb34cceffb9ef04d99f420f68eb75d901e9560b8749fc41",
        url="https://pypi.org/packages/5e/c4/6c4fe722df5343c33226f0b4e0bb042e4dc13483228b4718baf286f86d87/certifi-2020.6.20-py2.py3-none-any.whl",
    )
    version(
        "2020.4.5.1",
        sha256="1d987a998c75633c40847cc966fcf5904906c920a7f17ef374f5aa4282abd304",
        url="https://pypi.org/packages/57/2b/26e37a4b034800c960a00c4e1b3d9ca5d7014e983e6e729e33ea2f36426c/certifi-2020.4.5.1-py2.py3-none-any.whl",
    )
    version(
        "2019.9.11",
        sha256="fd7c7c74727ddcf00e9acd26bba8da604ffec95bf1c2144e67aff7a8b50e6cef",
        url="https://pypi.org/packages/18/b0/8146a4f8dd402f60744fa380bc73ca47303cccf8b9190fd16a827281eac2/certifi-2019.9.11-py2.py3-none-any.whl",
    )
    version(
        "2019.6.16",
        sha256="046832c04d4e752f37383b628bc601a7ea7211496b4638f6514d0e5b9acc4939",
        url="https://pypi.org/packages/69/1b/b853c7a9d4f6a6d00749e94eb6f3a041e342a885b87340b79c1ef73e3a78/certifi-2019.6.16-py2.py3-none-any.whl",
    )
    version(
        "2019.3.9",
        sha256="59b7658e26ca9c7339e00f8f4636cdfe59d34fa37b9b04f6f9e9926b3cece1a5",
        url="https://pypi.org/packages/60/75/f692a584e85b7eaba0e03827b3d51f45f571c2e793dd731e598828d380aa/certifi-2019.3.9-py2.py3-none-any.whl",
    )
    version(
        "2017.4.17",
        sha256="f4318671072f030a33c7ca6acaef720ddd50ff124d1388e50c1bda4cbd6d7010",
        url="https://pypi.org/packages/eb/01/c1f58987b777d6c4ec535b4e004a4a07bfc9db06f0c7533367ca6da8f2a6/certifi-2017.4.17-py2.py3-none-any.whl",
    )
    version(
        "2017.1.23",
        sha256="f74a224a9860fd5a2e9757230a7ea3eba82d6d46914780abc18e70c8b58d4bf8",
        url="https://pypi.org/packages/21/f7/7bb6b1c5ba1db21515950bc16b22cd7ef7d27024100f326a19921efd2ce0/certifi-2017.1.23-py2.py3-none-any.whl",
    )
