# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIpykernel(PythonPackage):
    """IPython Kernel for Jupyter"""

    homepage = "https://github.com/ipython/ipykernel"
    pypi = "ipykernel/ipykernel-5.3.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "6.23.1",
        sha256="77aeffab056c21d16f1edccdc9e5ccbf7d96eb401bd6703610a21be8b068aadc",
        url="https://pypi.org/packages/5d/4b/ffb537e392e730c9a5b02758f9c87077d9087bcb0d957853e13f121e5ea7/ipykernel-6.23.1-py3-none-any.whl",
    )
    version(
        "6.22.0",
        sha256="1ae6047c1277508933078163721bbb479c3e7292778a04b4bacf0874550977d6",
        url="https://pypi.org/packages/48/1b/260b3e4d2f633c1c9019e25a977a9e82341d0713ad8fb60e01b97b7559a4/ipykernel-6.22.0-py3-none-any.whl",
    )
    version(
        "6.16.0",
        sha256="d3d95241cd4dd302fea9d5747b00509b58997356d1f6333c9a074c3eccb78cb3",
        url="https://pypi.org/packages/3d/4f/02454d0a2f90746143fe56568d34594bd34503d4c51b5ad15f08e1283fad/ipykernel-6.16.0-py3-none-any.whl",
    )
    version(
        "6.15.2",
        sha256="59183ef833b82c72211aace3fb48fd20eae8e2d0cae475f3d5c39d4a688e81ec",
        url="https://pypi.org/packages/f7/97/9bcde0cb3b5bf5208787a296573c086ae6ce4615d10599570bce76197c85/ipykernel-6.15.2-py3-none-any.whl",
    )
    version(
        "6.9.1",
        sha256="4fae9df6e192837552b2406a6052d707046dd2e153860be73c68484bacba18ed",
        url="https://pypi.org/packages/62/4e/1149519ad9e90b6903e5e4b73454cb02d2c0cd62ef2f21c9d93c752cdb5f/ipykernel-6.9.1-py3-none-any.whl",
    )
    version(
        "6.4.1",
        sha256="a3f6c2dda2ecf63b37446808a70ed825fea04790779ca524889c596deae0def8",
        url="https://pypi.org/packages/4a/c8/2a8a5cb1afdecfa92c000e3a5d63a9fdd1b7fe77570f65536b3f05a05f14/ipykernel-6.4.1-py3-none-any.whl",
    )
    version(
        "6.2.0",
        sha256="35cc31accec420e90c4b66ea7f4e7b067c769e31af3502e45326c6f1294d238d",
        url="https://pypi.org/packages/d4/9a/59010716573b2aae10ccf88ea275c9a50943a7f8d4a123ad3c6f385a6c94/ipykernel-6.2.0-py3-none-any.whl",
    )
    version(
        "6.0.2",
        sha256="61792e0de765e8b258489715d81b0ff2e87ec0ed9f006bb20819c4d40586dc19",
        url="https://pypi.org/packages/13/8e/1d868a67488f99692c2604907cdb87ab7da586fa114d5f0f177c83f1aee1/ipykernel-6.0.2-py3-none-any.whl",
    )
    version(
        "5.5.6",
        sha256="66f824af1ef4650e1e2f6c42e1423074321440ef79ca3651a6cfd06a4e25e42f",
        url="https://pypi.org/packages/e9/ad/9101e0ab5e84dd117462bb3a1379d31728a849b6886458452e3d97dc6bba/ipykernel-5.5.6-py3-none-any.whl",
    )
    version(
        "5.5.5",
        sha256="29eee66548ee7c2edb7941de60c0ccf0a7a8dd957341db0a49c5e8e6a0fcb712",
        url="https://pypi.org/packages/90/6d/6c8fe4b658f77947d4244ce81f60230c4c8d1dc1a21ae83e63b269339178/ipykernel-5.5.5-py3-none-any.whl",
    )
    version(
        "5.3.4",
        sha256="d6fbba26dba3cebd411382bc484f7bc2caa98427ae0ddb4ab37fe8bfeb5c7dd3",
        url="https://pypi.org/packages/52/19/c2812690d8b340987eecd2cbc18549b1d130b94c5d97fcbe49f5f8710edf/ipykernel-5.3.4-py3-none-any.whl",
    )
    version(
        "5.1.1",
        sha256="346189536b88859937b5f4848a6fd85d1ad0729f01724a411de5cae9b618819c",
        url="https://pypi.org/packages/a0/35/dd97fbb48d4e6b5ae97307497e31e46691adc2feedb6279d29fc1c8ad9c1/ipykernel-5.1.1-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="0aeb7ec277ac42cc2b59ae3d08b10909b2ec161dc6908096210527162b53675d",
        url="https://pypi.org/packages/d8/b0/f0be5c5ab335196f5cce96e5b889a4fcf5bfe462eb0acc05cd7e2caf65eb/ipykernel-5.1.0-py3-none-any.whl",
    )
    version(
        "4.10.0",
        sha256="56d82987472f4b14ab0214e4aef55def006671885d285cd8821f2600861215a6",
        url="https://pypi.org/packages/22/5e/69b0ae84e0cd7c8d4467e0a7b390c560d8c7642493329b15461b41e20fcc/ipykernel-4.10.0-py3-none-any.whl",
    )
    version(
        "4.5.0",
        sha256="c18a6b4f227647ca8a04fc19f9d0acb668aecec612c0db87690fd450b705b474",
        url="https://pypi.org/packages/ab/3b/3ff53396b59d27173147ccb03579ed960e9cc3a95ffe72997131239894fb/ipykernel-4.5.0-py2.py3-none-any.whl",
    )
    version(
        "4.4.1",
        sha256="a6747bd23dc13d958058eb9294b4c491f51b2101b4ae67b8660836ba06495642",
        url="https://pypi.org/packages/a5/69/9dba173a7dde8b381194b9f2ef3bf7abdf0f2cf7aeef34d75d910c5e62ee/ipykernel-4.4.1-py2.py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="7a575cab0c2b61a5fc55a3cb8cb53277bbc43ae895845d28845533f1d72b9afa",
        url="https://pypi.org/packages/10/df/26b3894402f3ada9c139d7dc9e575e372951730a04a9030486a421ea3b83/ipykernel-4.4.0-py2.py3-none-any.whl",
    )
    version(
        "4.3.1",
        sha256="90ab4474c56570104d1eeb4df3fd3ec80a1ae6c4dff4f66757ebe19e5634e099",
        url="https://pypi.org/packages/b9/2c/29b5721a469dae5c7417e52684d56f38c09e3c76703bf0b3904f7466eeca/ipykernel-4.3.1-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="03566ba3b93a620c7ec538d471a56f6b39862c61215ee9012d2029477bba2172",
        url="https://pypi.org/packages/3a/7a/39d628e4c3f0c46036ec663da8a84287ebd251260c59e4961a35d4cd46d6/ipykernel-4.3.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.2",
        sha256="3b9e92d78559eeee191d07aab88211c73c0f7eae8d9dddf7d2faa23d61b8361d",
        url="https://pypi.org/packages/d2/87/8800c72ff09e6c8792f33217f3dbedee393fd08c8aaa4a0f04dcac4bf47a/ipykernel-4.2.2-py2.py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="9d04a948006e2b713130b0f077eedd3cadc263ec6fa533ac57258f752ee7daa9",
        url="https://pypi.org/packages/fa/50/c73db49e9764e050233af5f903169ae7ae0889520dc7d3b5f646ff62d5e3/ipykernel-4.2.1-py2.py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="0a17b355446aeb04ef617ebdbbb5a59513aa26dbe684d99f67b69de8038c5fff",
        url="https://pypi.org/packages/61/12/40c5953757324bd440faabed26fc3036af98cb7b8559fe34f7e2532e0c93/ipykernel-4.2.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.1",
        sha256="48b5eb74f9ce1abd0177624b86929a1565f702d27c4323286e06f98bcccadd8a",
        url="https://pypi.org/packages/a6/f1/58a60bacb0e675d9e97a9a6cb1187979cb1b71fb45f0bd3531ef8a55b0d1/ipykernel-4.1.1-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="5775d2d6008a667e1e7c646991517403121023948ddc165b1546ea3950b0fc72",
        url="https://pypi.org/packages/38/df/c12d430c4db02ea266788ebf78a8a4377dfd94af5934ae4f037e29d48186/ipykernel-4.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@6.17:")
        depends_on("python@3.7:", when="@6.0.0-alpha1:6.16")
        depends_on("py-appnope", when="@5.1.3:5.3.1,5.3.3: platform=darwin")
        depends_on("py-argcomplete@1.12.3:", when="@6.1:6.6 ^python@:3.7")
        depends_on("py-comm@0.1.1:", when="@6.19:")
        depends_on("py-debugpy@1.6.5:", when="@6.21:")
        depends_on("py-debugpy@1.0.0:", when="@6:6.20")
        depends_on("py-importlib-metadata@:4", when="@6.1:6.6 ^python@:3.7")
        depends_on("py-importlib-metadata@:3", when="@6.0.0-alpha5:6.0 ^python@:3.7")
        depends_on("py-ipython@7.23.1:", when="@6.5.1:")
        depends_on("py-ipython@7.23.1:7", when="@6.0.2:6.5.0")
        depends_on("py-ipython@5.0.0:", when="@5.0.0:5.3.1,5.3.3:5")
        depends_on("py-ipython@4.0.0:", when="@4.2.2:5.0.0-beta1")
        depends_on("py-ipython-genutils", when="@5.5.6:5,6.3.1:6.4")
        depends_on("py-jupyter-client@6.1.12:", when="@6.11:")
        depends_on("py-jupyter-client@:7", when="@6.2:6.10")
        depends_on("py-jupyter-client@:6", when="@6.0.2:6.1")
        depends_on("py-jupyter-client", when="@4.2.2:5.3.1,5.3.3:6.0.0")
        depends_on("py-jupyter-core@4.12:4,5.1:", when="@6.21:")
        depends_on("py-matplotlib-inline", when="@6.0.2:")
        depends_on("py-nest-asyncio", when="@6.6.1:6.20,6.21.1:")
        depends_on("py-packaging", when="@6.12:")
        depends_on("py-psutil", when="@6.9.2:")
        depends_on("py-pyzmq@20:", when="@6.21.2:6.27")
        depends_on("py-pyzmq@17.0.0:", when="@6.15:6.21.1")
        depends_on("py-tornado@6.1:", when="@6.11:")
        depends_on("py-tornado@4.2:", when="@5:5.3.1,5.3.3:6.9")
        depends_on("py-tornado@4:", when="@4.3:4")
        depends_on("py-traitlets@5.4:", when="@6.19:")
        depends_on("py-traitlets@5.1:", when="@6.5:6.18")
        depends_on("py-traitlets@4.1.0:", when="@4.4:5.3.1,5.3.3:6.4")
        depends_on("py-traitlets", when="@4.2.2:4.3")

    conflicts("^py-jupyter-core@5.0")

    # Historical dependencies
