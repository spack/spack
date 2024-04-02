# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyKubernetes(PythonPackage):
    """Official Python client library for kubernetes."""

    homepage = "https://kubernetes.io"
    git = "https://github.com/kubernetes-client/python.git"
    pypi = "kubernetes/kubernetes-17.17.0.tar.gz"

    maintainers("vvolkl")

    license("Apache-2.0")

    version(
        "29.0.0",
        sha256="ab8cb0e0576ccdfb71886366efb102c6a20f268d817be065ce7f9909c631e43e",
        url="https://pypi.org/packages/6f/34/164e57fec8a9693d7e6ae2d1a345482020ea9e9b32eab95a90bb3eaea83d/kubernetes-29.0.0-py2.py3-none-any.whl",
    )
    version(
        "28.1.0",
        sha256="10f56f8160dcb73647f15fafda268e7f60cf7dbc9f8e46d52fcd46d3beb0c18d",
        url="https://pypi.org/packages/f5/6a/1f69c2d8b1ff03f8d8e10d801f4ac3016ed4c1b00aa9795732c6ec900bba/kubernetes-28.1.0-py2.py3-none-any.whl",
    )
    version(
        "27.2.0",
        sha256="0f9376329c85cf07615ed6886bf9bf21eb1cbfc05e14ec7b0f74ed8153cd2815",
        url="https://pypi.org/packages/99/89/3ab0cb3069f49ae2eaf73f884c82164f18f70fcc598e0312edea71614ad7/kubernetes-27.2.0-py2.py3-none-any.whl",
    )
    version(
        "26.1.0",
        sha256="e3db6800abf7e36c38d2629b5cb6b74d10988ee0cba6fba45595a7cbe60c0042",
        url="https://pypi.org/packages/74/21/ada0c5eedb678ab663f8e387734418fdd1a26be28fc919a0c32e52964047/kubernetes-26.1.0-py2.py3-none-any.whl",
    )
    version(
        "25.3.0",
        sha256="eb42333dad0bb5caf4e66460c6a4a1a36f0f057a040f35018f6c05a699baed86",
        url="https://pypi.org/packages/e9/ad/2f2d4f22883256a505a4997cdc48c556e88e308c98eea6579e5dafcaa5e9/kubernetes-25.3.0-py2.py3-none-any.whl",
    )
    version(
        "21.7.0",
        sha256="044c20253f8577491a87af8f9edea1f929ed6d62ce306376a6cb8aed24e572c5",
        url="https://pypi.org/packages/ec/73/aa291e48896cb2b60d8da9907df6d10cbc08c0d6685ae9a2140ac37f8628/kubernetes-21.7.0-py2.py3-none-any.whl",
    )
    version(
        "20.13.0",
        sha256="7d32ea7f555813a141a0e912e7695d88f7213bb632a860ba79a963b43f7a6b18",
        url="https://pypi.org/packages/32/a8/b771d543156d8fee42876f7bc57023194fc2627efb6049e1ec8b87860bab/kubernetes-20.13.0-py2.py3-none-any.whl",
    )
    version(
        "19.15.0",
        sha256="52312adda60d92ba45b325f2c1505924656389222005f7e089718e1ad03bc07f",
        url="https://pypi.org/packages/f8/bc/138f57c7801825bee7b3b1ac7c6c21db747bd8064af8c6b574aa11c3bea8/kubernetes-19.15.0-py2.py3-none-any.whl",
    )
    version(
        "18.20.0",
        sha256="ff31ec17437293e7d4e1459f1228c42d27c7724dfb56b4868aba7a901a5b72c9",
        url="https://pypi.org/packages/19/4a/39b09950b35a36fe1af54bb85413c2976b62a5c29e7254c8c3573f86c028/kubernetes-18.20.0-py2.py3-none-any.whl",
    )
    version(
        "17.17.0",
        sha256="225a95a0aadbd5b645ab389d941a7980db8cdad2a776fde64d1b43fc3299bde9",
        url="https://pypi.org/packages/19/07/35bcfa79df97a726d14b00dd12be5232034cbb0510a788082ad3d6be4ef3/kubernetes-17.17.0-py3-none-any.whl",
    )
    version(
        "12.0.1",
        sha256="23c85d8571df8f56e773f1a413bc081537536dc47e2b5e8dc2e6262edb2c57ca",
        url="https://pypi.org/packages/50/55/84aaadb5f8b4d2641f28eb7373feb610f4b609cc9cf223bcd494fd66a647/kubernetes-12.0.1-py2.py3-none-any.whl",
    )
    version(
        "12.0.0",
        sha256="9a339a32d6c79e6461cb6050c3662cb4e33058b508d8d34ee5d5206add395828",
        url="https://pypi.org/packages/3b/4e/6a16c118f72dd7b6334b2a6662d2a0693cf31f8b76dfe0fbcdaebb91d33b/kubernetes-12.0.0-py3-none-any.whl",
    )
    version(
        "11.0.0",
        sha256="4af81201520977139a143f96123fb789fa351879df37f122916b9b6ed050bbaf",
        url="https://pypi.org/packages/59/46/d4b9364fcab59b5f9248e014c7592df8de84ad6548a6fe3de2d805bb75fc/kubernetes-11.0.0-py3-none-any.whl",
    )
    version(
        "10.1.0",
        sha256="9aa4f34431a442dda856bafc959bcf296cb5802f370361604c440093c702b17c",
        url="https://pypi.org/packages/15/60/57bcecea1472e1b2038197bd4adccdf90ccb845fd34f33b9a19a7feb7c20/kubernetes-10.1.0-py3-none-any.whl",
    )
    version(
        "10.0.1",
        sha256="a6dee02a1b39ea4bb9c4c2cc415ea0ada33d8ea0a920f7d4fb6d166989dcac01",
        url="https://pypi.org/packages/6e/fc/2cab119f679648b348b8940de0dd744a1f0ee99c690aa2ef6072f050816c/kubernetes-10.0.1-py2.py3-none-any.whl",
    )
    version(
        "9.0.0",
        sha256="f56137a298cb1453dd908b49dd4169347287c971e8cabd11b32f27570fec314c",
        url="https://pypi.org/packages/00/f7/4f196c55f1c2713d3edc8252c4b45326306eef4dc10048f13916fe446e2b/kubernetes-9.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-certifi@14:")
        depends_on("py-google-auth@1.0.1:")
        depends_on("py-oauthlib@3.2.2:", when="@27:")
        depends_on("py-python-dateutil@2.5.3:")
        depends_on("py-pyyaml@5.4.1:", when="@18.20:")
        depends_on("py-pyyaml@3.12:3", when="@10.1:10")
        depends_on("py-pyyaml@3.12:", when="@:10.0,11:18.17")
        depends_on("py-requests")
        depends_on("py-requests-oauthlib")
        depends_on("py-setuptools@21:", when="@:27.2.0-beta1")
        depends_on("py-six@1.9:")
        depends_on("py-urllib3@1.24.2:1", when="@28")
        depends_on("py-urllib3@1.24.2:", when="@8.0.2:8,9.0.1:9,10.0.1:27,29:")
        depends_on("py-urllib3@1.23:", when="@7.0.1:7,8.0.1,9:9.0.0,10:10.0.0")
        depends_on("py-websocket-client@0.32:0.39,0.43:")
