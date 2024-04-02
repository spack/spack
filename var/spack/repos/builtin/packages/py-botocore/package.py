# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBotocore(PythonPackage):
    """Low-level, data-driven core of boto 3."""

    homepage = "https://github.com/boto/botocore"
    pypi = "botocore/botocore-1.13.44.tar.gz"

    version(
        "1.34.44",
        sha256="8d9837fb33256e70b9c8955a32d3e60fa70a0b72849a909737cf105fcc3b5deb",
        url="https://pypi.org/packages/aa/3a/5b08bc151e45ffe8c661af1a587cf2ac6ad9410e7d341e343ca46bfca83e/botocore-1.34.44-py3-none-any.whl",
    )
    version(
        "1.31.41",
        sha256="c33a453328d361c089e6a8f9dd671a7b939288e539e6550c7030152e8162e906",
        url="https://pypi.org/packages/1e/c3/5eeaaae524a9f867a1454cfd4f989a1864583b8b6ba45b92be800daaab9c/botocore-1.31.41-py3-none-any.whl",
    )
    version(
        "1.29.84",
        sha256="0f976427ad0a2602624ba784b5db328a865c2e9e0cc1bb6d8cffb6c0a2d177e1",
        url="https://pypi.org/packages/9f/a6/a32edea5fcf270ed4ff075462f3d2e13f3ffcf4a1f36a85e28407709e264/botocore-1.29.84-py3-none-any.whl",
    )
    version(
        "1.29.76",
        sha256="70735b00cd529f152992231ca6757e458e5ec25db43767b3526e9a35b2f143b7",
        url="https://pypi.org/packages/87/93/e862d4b2ec9b0c8f7a6ee3141df138c00aa91de42839e55b68e3ebb53bf2/botocore-1.29.76-py3-none-any.whl",
    )
    version(
        "1.29.56",
        sha256="669ed3a256c4352f8f8a77a24b4d623ab7acc966d843b460d7ce2261a9813a79",
        url="https://pypi.org/packages/97/39/50e4b90ac76db171bd56339e4f184aca1a23e51c15f1a2b91dc4d324e5a4/botocore-1.29.56-py3-none-any.whl",
    )
    version(
        "1.29.26",
        sha256="2ca26983156fe0846a87b9325205af6bc56268fb99b8b4b9decccf50203ff3b4",
        url="https://pypi.org/packages/dc/71/f39a2f150ebf4c6314b80e56eb7d8de3b27f966766ea9607eb5a51fe12d4/botocore-1.29.26-py3-none-any.whl",
    )
    version(
        "1.28.5",
        sha256="5eb98c85e80fab6640342377ce947c86a003bbaf8427c2e7a03c8da0bdbb796c",
        url="https://pypi.org/packages/08/7c/5672539c66ab305e385fcb578b395feec894e3277f35843a1e4c94259fb3/botocore-1.28.5-py3-none-any.whl",
    )
    version(
        "1.27.96",
        sha256="e41a81a18511f2f9181b2a9ab302a55c0effecccbef846c55aad0c47bfdbefb9",
        url="https://pypi.org/packages/f9/73/aa345e22ce21e86fa99e8dc25ab7ae4fd73eedc4c365282c82fa6ba3f66f/botocore-1.27.96-py3-none-any.whl",
    )
    version(
        "1.27.59",
        sha256="69d756791fc024bda54f6c53f71ae34e695ee41bbbc1743d9179c4837a4929da",
        url="https://pypi.org/packages/0f/70/d09a704da82119d64848826dbbd5a8c18e5b57ca6aca0061634d6418c01a/botocore-1.27.59-py3-none-any.whl",
    )
    version(
        "1.26.10",
        sha256="8a4a984bf901ccefe40037da11ba2abd1ddbcb3b490a492b7f218509c99fc12f",
        url="https://pypi.org/packages/09/b8/794e0bd260198538ded90c26b353ddb632eab01950d4e7e2e2b8ee510d12/botocore-1.26.10-py3-none-any.whl",
    )
    version(
        "1.25.13",
        sha256="79b7773b48c9c59acd42ceba0a05b27ab9e326e9ed9b0ca35f41ad8abad61808",
        url="https://pypi.org/packages/35/fe/a1ec1387bc0bc48e950ac2d2bc69a886d08185ed148a25ceabbb2976e6e3/botocore-1.25.13-py3-none-any.whl",
    )
    version(
        "1.24.46",
        sha256="663d8f02b98641846eb959c54c840cc33264d5f2dee5b8fc09ee8adbef0f8dcf",
        url="https://pypi.org/packages/96/cb/dd5b165bf3bf7e3da57db4372e481928a09e1fc1452e805328a805f90515/botocore-1.24.46-py3-none-any.whl",
    )
    version(
        "1.23.54",
        sha256="06ae8076c4dcf3d72bec4d37e5f2dce4a92a18a8cdaa3bfaa6e3b7b5e30a8d7e",
        url="https://pypi.org/packages/a6/08/3cc6858a2d9fee8538f212944cff08df325828fbfe17801974c95f51f338/botocore-1.23.54-py3-none-any.whl",
    )
    version(
        "1.22.12",
        sha256="1d1094fb53ebe4535d8840fbd7c14aadb65bde7ff03a65f9a4f1d76bd03e16ff",
        url="https://pypi.org/packages/6a/73/552b27e3a1b4f83630907c4958be78e9d4c906e73efd554ebd5e21cb1692/botocore-1.22.12-py3-none-any.whl",
    )
    version(
        "1.21.65",
        sha256="3bd0e3d6daee6afcc747d596b52158519abe1ce36f906d556b9f8b54faa081e8",
        url="https://pypi.org/packages/0b/12/0ece2363299f037904fe7cb75faaae859e1547f43e688b6195343ff60e76/botocore-1.21.65-py3-none-any.whl",
    )
    version(
        "1.21.12",
        sha256="7b205f96bf0e2e1017301339e4fba9fd6dfdf54680196eb43e60e60581d7d5cb",
        url="https://pypi.org/packages/14/a8/6c40fe2fa209e8c6893d42e82a474faaaa53c943ebf2e4c0fceedfaa01d1/botocore-1.21.12-py3-none-any.whl",
    )
    version(
        "1.20.112",
        sha256="6d51de0981a3ef19da9e6a3c73b5ab427e3c0c8b92200ebd38d087299683dd2b",
        url="https://pypi.org/packages/c7/ea/11c3beca131920f552602b98d7ba9fc5b46bee6a59cbd48a95a85cbb8f41/botocore-1.20.112-py2.py3-none-any.whl",
    )
    version(
        "1.20.27",
        sha256="57e45c9d443163da7312cae61bcc60382e6d0b3aecda68e850d6438162fe7b5b",
        url="https://pypi.org/packages/6f/b3/4cf3d9ba97f09a4081c4428f1014eef0e1f9b5deb95e4733799e3666f1a9/botocore-1.20.27-py2.py3-none-any.whl",
    )
    version(
        "1.19.63",
        sha256="ad4adfcc195b5401d84b0c65d3a89e507c1d54c201879c8761ff10ef5c361e21",
        url="https://pypi.org/packages/2c/05/0a955f0c92bec7da076fbbc73926dfb13fab8e2b88de7f8eb17c443f28f0/botocore-1.19.63-py2.py3-none-any.whl",
    )
    version(
        "1.19.52",
        sha256="d8f50e4162012ccfab64c2db4fcc99313d46d57789072251bab56013d66546e2",
        url="https://pypi.org/packages/e9/a8/3a70380b52a34bed791a1dcc3f5e5967c81676f452aef440416efac62cfd/botocore-1.19.52-py2.py3-none-any.whl",
    )
    version(
        "1.13.50",
        sha256="adb4cb188cd0866e7337f9a049fc68db042b0340fd496d40bca349c8dbfc6a2d",
        url="https://pypi.org/packages/24/2d/47bc2f26b9f014998ad5c6ed844424a69f8ea77d26dab22a4e2ddbff20d4/botocore-1.13.50-py2.py3-none-any.whl",
    )
    version(
        "1.13.44",
        sha256="49791fada1e15bb2aafb36a16c2c2d568279c9274e0ad6a9ac7fbc0f6cb17f57",
        url="https://pypi.org/packages/6f/7c/d39d8dd612cd1631a86f2901538621482e8fd97f1dc1c73b1260f535d976/botocore-1.13.44-py2.py3-none-any.whl",
    )
    version(
        "1.13.38",
        sha256="81b588e5a0e33e75c619f992d315b14b81597fe8bd1291a801724861df4d8cef",
        url="https://pypi.org/packages/89/7b/91602326d58e4a59a0e510e88858b4c072110679044053148545b5a170fb/botocore-1.13.38-py2.py3-none-any.whl",
    )
    version(
        "1.12.253",
        sha256="dc080aed4f9b220a9e916ca29ca97a9d37e8e1d296fe89cbaeef929bf0c8066b",
        url="https://pypi.org/packages/8e/7b/88f10115b4748f86be6b7b1d8761ba5023fccf6e6cbe762e368f63eddcf9/botocore-1.12.253-py2.py3-none-any.whl",
    )
    version(
        "1.12.169",
        sha256="22e7d079b62562591bc5b00a4fa97e0626b6ffb1b605929c7b023171c33a548a",
        url="https://pypi.org/packages/28/ac/a43d37f371f5854514128d7c54887176b8df3bc9925a25e5096298033f93/botocore-1.12.169-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.34:")
        depends_on("python@3.7:", when="@1.27:1.33")
        depends_on("py-jmespath@0.7.1:", when="@1.24.21:")
        depends_on("py-jmespath@0.7.1:0", when="@1.17.25:1.21.40,1.21.42:1.24.20")
        depends_on("py-python-dateutil@2:", when="@1.17.25:1.21.40,1.21.42:")
        depends_on("py-urllib3@1.25.4:1", when="@1.31.62: ^python@:3.9")
        depends_on("py-urllib3@1.25.4:2.0", when="@1.31.62:1.34.62 ^python@3.10:")
        depends_on("py-urllib3@1.25.4:1", when="@1.19.17:1.21.40,1.21.42:1.31.61")
