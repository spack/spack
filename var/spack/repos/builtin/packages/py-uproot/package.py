# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot(PythonPackage):
    """ROOT I/O in pure Python and NumPy.

    Uproot is a reader and a writer of the ROOT file format using only Python
    and Numpy. Unlike the standard C++ ROOT implementation, Uproot is only an
    I/O library, primarily intended to stream data into machine learning
    libraries in Python. Unlike PyROOT and root_numpy, Uproot does not depend
    on C++ ROOT. Instead, it uses Numpy to cast blocks of data from the ROOT
    file as Numpy arrays."""

    homepage = "https://github.com/scikit-hep/uproot4"
    pypi = "uproot/uproot-4.0.6.tar.gz"

    maintainers("vvolkl")

    tags = ["hep"]

    license("BSD-3-Clause")

    version(
        "5.0.5",
        sha256="900aad0fd71d4730d5e5d98bbd926d1afabd229756ec63c8959dec57a7a78e88",
        url="https://pypi.org/packages/ba/ba/9910833d8ece6c5d52613b4bdeece5e2c0df65d384e803a91acd83486a17/uproot-5.0.5-py3-none-any.whl",
    )
    version(
        "5.0.4",
        sha256="5a4a526fbec5d5bb3c439dcee0876bc689d42a36627a4a89105924afc3b3ec24",
        url="https://pypi.org/packages/cc/be/000ad141863f38a931fb73d34018a1d9c00884a5dbc263dccd3835bc0ec6/uproot-5.0.4-py3-none-any.whl",
    )
    version(
        "5.0.3",
        sha256="b826e62ddacc9717045fc95f1ff9b690c683368ece7ee74deba670300c0712bb",
        url="https://pypi.org/packages/9d/f2/57d054b926de2bafbe702090d4a17da6cd3924f1d8103b120f291fc2556c/uproot-5.0.3-py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="5c74fc126ec6aa76488466e345e0e51efb51239c66e32f31fbdf534e21bad030",
        url="https://pypi.org/packages/50/ce/343326e18b2c809fc4553ba707312fba394305fd3e1e69bcedd8a30653f5/uproot-5.0.2-py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="ceefab14d57942cee11dd43b02503291097f725fca2677d8da4cfb2383cc5a89",
        url="https://pypi.org/packages/dd/ba/59d44c1d4b41707b5fd1658945ca34bd845c40a8ba4bb1dd6d6dc6484417/uproot-5.0.1-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="722a341b84e0d84a105425d147cc91256c7c80747564a42f24ce9778f18adad7",
        url="https://pypi.org/packages/c0/75/1182d0cb43e48d437359a3584546a995537e772d5df8dab159674f96d3da/uproot-5.0.0-py3-none-any.whl",
    )
    version(
        "4.3.7",
        sha256="7b55df2b5b8c0db9d4d4e4bdb7161e29215a0fbd39087971b657514d0c67d4c2",
        url="https://pypi.org/packages/fa/2f/c4b3dbc0c3b6cdce29e66f5bea5d920c064d699c1d1dd2ecb27fcb8b5d47/uproot-4.3.7-py3-none-any.whl",
    )
    version(
        "4.3.6",
        sha256="780049013204481eb89d7db61169a3bf306d0fd7c8f22c79aa895e24ca68a3b8",
        url="https://pypi.org/packages/81/f9/ba105299f43f9544574f7bc4ccb1f09bc87d252e71103290097f11175788/uproot-4.3.6-py3-none-any.whl",
    )
    version(
        "4.3.5",
        sha256="940300d6b700f719ae90bfebc00a8deada3cfe43010cd2258ef6ab35e637319d",
        url="https://pypi.org/packages/be/3e/50da9b92af3efd7026da13406ae7ee859cd0e04bae680763e81b277e8079/uproot-4.3.5-py3-none-any.whl",
    )
    version(
        "4.3.4",
        sha256="87ebc97e86854e2adcc12fa29a274e5b4e6ce7c3f1fc2784f7aeccceb57a30a3",
        url="https://pypi.org/packages/12/30/7193f4e029c3be48ec70cdbba8edd8ea911d2a0a329024be05d33c3f4bfd/uproot-4.3.4-py2.py3-none-any.whl",
    )
    version(
        "4.3.3",
        sha256="7502807920d8c3e4c8d1c1ffe540c90152398ba45e0f3e508875b32ae9892332",
        url="https://pypi.org/packages/0a/12/5186335f38074dde8a1157834118c54809d45fef23a81e79afa3e2f7607b/uproot-4.3.3-py2.py3-none-any.whl",
    )
    version(
        "4.3.2",
        sha256="9c6abda4c2d8b4f14de10d91c19692bc5830ebe70ca257811adc052746782dca",
        url="https://pypi.org/packages/73/6f/ee5cf3b4b3859c4106f5bbde6eb64452800917c564af3c3d34efbca6d7ee/uproot-4.3.2-py2.py3-none-any.whl",
    )
    version(
        "4.3.1",
        sha256="23bef36caa0dcad5d1273c5359a11323a01bdc710adb953371291cc7fc73b62b",
        url="https://pypi.org/packages/d5/09/38f19efe9a465f2ae7317c62ca039aeecf91278f280c65c10c9cec808333/uproot-4.3.1-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="d7f82480e812805444ffd0f3ec44934d3b10a547ea5c1c489153634d905f1343",
        url="https://pypi.org/packages/b5/73/a2cbb91cccb77ea7f346224f54425bd5abcd4929fc971ac02ea8300a101c/uproot-4.3.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.4",
        sha256="3da12232e5247292826fb4de6cc0464f83fb931311977591ec26d8b58025031d",
        url="https://pypi.org/packages/34/44/428527157bcee4bbde363505a60d19d9af2f46da31d0e9e960f5118ce000/uproot-4.2.4-py2.py3-none-any.whl",
    )
    version(
        "4.2.3",
        sha256="2f7ad4057ae11319c44111c0feaa90b51d1ac132cf17f0bd7d82b78525d3b4ac",
        url="https://pypi.org/packages/3e/48/7c459ffc8996ff83cd6442657356e345456df46edbf63b93a4359931384b/uproot-4.2.3-py2.py3-none-any.whl",
    )
    version(
        "4.2.2",
        sha256="39df5c4e501ba924c7ba12a9bf9ef91e332a593a422f0dbdde1c774ee5920ef8",
        url="https://pypi.org/packages/2d/0a/f191041e74fc05783fca8d3d4fd6d2a2af32132e10653e2a86ed7404e539/uproot-4.2.2-py2.py3-none-any.whl",
    )
    version(
        "4.1.8",
        sha256="cced42c62cf080728df8ac07cadedd845f6af9ae885fb06398d331cc945bd2ff",
        url="https://pypi.org/packages/da/ec/62916a8b4001a56d11bc888e54ed21b1fcc193d61cef84ecf5bf4d98e109/uproot-4.1.8-py2.py3-none-any.whl",
    )
    version(
        "4.0.11",
        sha256="c0b6111b2034211eba2d8ecce5502ed35bfd395b45eabed20ec6c20d21437c41",
        url="https://pypi.org/packages/b8/0b/27399201b0b5c049f339d0263de96079b18b7ef82a1afdb436406a8472aa/uproot-4.0.11-py2.py3-none-any.whl",
    )
    version(
        "4.0.10",
        sha256="01694bb3e31ac66029467a75b857c9c96c2f71314d50d876fe199f980815e823",
        url="https://pypi.org/packages/64/29/509d02ac708979f6982c199d65faefb76dc6a500a65eef8703633b0dd51c/uproot-4.0.10-py2.py3-none-any.whl",
    )
    version(
        "4.0.9",
        sha256="8e7df52f2edfdb373e440bc28b564c79776f1fe1d819b2753df3a01f8c00533d",
        url="https://pypi.org/packages/9c/1c/10b9a9ff56c2d48fd3e050ccceffefb763dffd8eb3efb9beb9082dced8f7/uproot-4.0.9-py2.py3-none-any.whl",
    )
    version(
        "4.0.8",
        sha256="ff590a7a142441c244532944c5c501890862899e83eb0f1d41f2c47c59c84d73",
        url="https://pypi.org/packages/a5/99/bf1b3995f9cafad30c8df34a99ab286f522cf762a2eb2152ac47609be04e/uproot-4.0.8-py2.py3-none-any.whl",
    )
    version(
        "4.0.7",
        sha256="7fbe065eb75f271819542df691499518ecc56caaa8e0166876d3d13be5bf08b3",
        url="https://pypi.org/packages/73/85/06dda0d02fa68f726d49eacce836eb501c1dfde33fe1162ee80358f4ca6b/uproot-4.0.7-py2.py3-none-any.whl",
    )
    version(
        "4.0.6",
        sha256="03988d9d7eee951182eb483884f68715a1c6d5c37b0f5918c020dea99f109203",
        url="https://pypi.org/packages/ae/01/efb4100d671aec20b3f04c289dfe19d0930e534de538ee8f748e72f783d6/uproot-4.0.6-py2.py3-none-any.whl",
    )

    variant(
        "lz4",
        default=True,
        description="Build with support for reading " "lz4-compressed rootfiles ",
    )
    variant("xrootd", default=True, description="Build with xrootd support ")
    variant(
        "zstd",
        default=True,
        description="Build with support for reading " "zstd-compressed rootfiles ",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.0.0-rc4:5.1.0-rc2")
        depends_on("py-awkward@2.0.0:", when="@5.0.0:5.1.0-rc1")
        depends_on("py-importlib-metadata", when="@5.0.0-rc2:5.3.1 ^python@:3.7")
        depends_on("py-numpy")
        depends_on("py-packaging", when="@5.0.0-rc2:")
        depends_on("py-setuptools", when="@4.0.8:5.0.0-rc1")
