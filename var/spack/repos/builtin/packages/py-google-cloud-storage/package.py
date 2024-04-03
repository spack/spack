# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudStorage(PythonPackage):
    """Google Cloud Storage API client library."""

    homepage = "https://github.com/googleapis/python-storage"
    pypi = "google-cloud-storage/google-cloud-storage-2.14.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.14.0",
        sha256="8641243bbf2a2042c16a6399551fbb13f062cbc9a2de38d6c0bb5426962e9dbd",
        url="https://pypi.org/packages/3d/48/574463fbf30c7021341ab0620e56103a8c49ad864bdd177935306c057986/google_cloud_storage-2.14.0-py2.py3-none-any.whl",
    )
    version(
        "2.13.0",
        sha256="ab0bf2e1780a1b74cf17fccb13788070b729f50c252f0c94ada2aae0ca95437d",
        url="https://pypi.org/packages/04/72/71b1b531cefa1daff8f6a2a70b4d4fa18dd4da851b5486d53578811b0838/google_cloud_storage-2.13.0-py2.py3-none-any.whl",
    )
    version(
        "2.12.0",
        sha256="bc52563439d42981b6e21b071a76da2791672776eda3ba99d13a8061ebbd6e5e",
        url="https://pypi.org/packages/68/b8/cb00819641313e67b640857ffff2c5afdcdcfb4940def9f1502bf614a6d9/google_cloud_storage-2.12.0-py2.py3-none-any.whl",
    )
    version(
        "2.11.0",
        sha256="88cbd7fb3d701c780c4272bc26952db99f25eb283fb4c2208423249f00b5fe53",
        url="https://pypi.org/packages/3a/9f/7923b9e460023470826d124156503359bf77ee130adb0872570599e8cd98/google_cloud_storage-2.11.0-py2.py3-none-any.whl",
    )
    version(
        "2.10.0",
        sha256="9433cf28801671de1c80434238fb1e7e4a1ba3087470e90f70c928ea77c2b9d7",
        url="https://pypi.org/packages/88/14/c9d4faae7ea4bff4405152cbc762b61100aa6949273b4eb3203d23308670/google_cloud_storage-2.10.0-py2.py3-none-any.whl",
    )
    version(
        "2.9.0",
        sha256="83a90447f23d5edd045e0037982c270302e3aeb45fc1288d2c2ca713d27bad94",
        url="https://pypi.org/packages/74/fb/3770e7f44cf6133f502e1b8503b6739351b53272cf8313b47f1de6cf4960/google_cloud_storage-2.9.0-py2.py3-none-any.whl",
    )
    version(
        "2.8.0",
        sha256="248e210c13bc109909160248af546a91cb2dabaf3d7ebbf04def9dd49f02dbb6",
        url="https://pypi.org/packages/30/84/4850b9c286a4baeebae14be62a616867323424f6a5091b151703858d86a6/google_cloud_storage-2.8.0-py2.py3-none-any.whl",
    )
    version(
        "2.7.0",
        sha256="f78a63525e72dd46406b255bbdf858a22c43d6bad8dc5bdeb7851a42967e95a1",
        url="https://pypi.org/packages/6e/23/3add67cdd1f2116eb4425b0d4f3154117b8a79eaaf3022edc23a71d82cc2/google_cloud_storage-2.7.0-py2.py3-none-any.whl",
    )
    version(
        "1.18.0",
        sha256="6be20fdfb51b857174e2c859b8b2fde85aefd61464909f3959c0e2f259edd694",
        url="https://pypi.org/packages/57/e6/a94429633ca5f812ecf661b78ff15f28f92130083a5709e6588c6c7ca5d9/google_cloud_storage-1.18.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.1:")
        depends_on("py-google-api-core@1.31.5:1,2.3.1:", when="@2.2:2.14")
        depends_on("py-google-auth@2.23.3:", when="@2.12:2.14")
        depends_on("py-google-auth@1.25:", when="@1.42:2.11")
        depends_on("py-google-auth@1.2:", when="@1.16:1.23")
        depends_on("py-google-cloud-core@2.3:", when="@2.3:")
        depends_on("py-google-cloud-core@1", when="@1.16:1.18")
        depends_on("py-google-crc32c@1:", when="@2.12:")
        depends_on("py-google-resumable-media@2.6:", when="@2.11:")
        depends_on("py-google-resumable-media@2.3.2:", when="@2.2:2.10")
        depends_on(
            "py-google-resumable-media@0.3.1:",
            when="@:1.14.0,1.15:1.15.1,1.16:1.16.1,1.17:1.17.0,1.18:1.18.0,1.19:1.19.0",
        )
        depends_on("py-requests@2.18:", when="@1.31.1:")
