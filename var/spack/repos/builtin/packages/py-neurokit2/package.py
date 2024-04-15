# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurokit2(PythonPackage):
    """The Python Toolbox for Neurophysiological Signal Processing.

    This package is the continuation of NeuroKit 1. It's a user-friendly
    package providing easy access to advanced biosignal processing routines.
    Researchers and clinicians without extensive knowledge of programming or
    biomedical signal processing can analyze physiological data with only two
    lines of code.
    """

    homepage = "https://github.com/neuropsychology/NeuroKit"
    pypi = "neurokit2/neurokit2-0.1.2.tar.gz"

    license("MIT")

    version(
        "0.2.4",
        sha256="fb48aa13dcae14620bf26f8b74bb90e6d811cb45c88b2260e42450b2baa82039",
        url="https://pypi.org/packages/19/f5/f8a0829619e0afa92fb57e6f83c40cbac7662cc5196aad99745d1e8642ad/neurokit2-0.2.4-py2.py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="4330d077db3db8dad15bbd151a4ff15d56e16fb429b0a5f85b545c503a77d432",
        url="https://pypi.org/packages/e7/ca/6802b97265bd2276262d2f00d7b408c8211eeb4b50076a6847b2e91dfda6/neurokit2-0.2.2-py2.py3-none-any.whl",
    )
    version(
        "0.1.5",
        sha256="863b59b1f2bf64d2604d12ef8075780c2c7d7b2a2513fad0e24e8a1190eaf5fb",
        url="https://pypi.org/packages/60/60/e95ca51edb08809d085b7af0cfc000b66a6d9826da85b888ead5f15b7eb9/neurokit2-0.1.5-py2.py3-none-any.whl",
    )
    version(
        "0.1.4.1",
        sha256="a9d12678a91690fde36323739625121662d0258731a517d4f180bb7cdcc354e1",
        url="https://pypi.org/packages/8b/db/b97ba6e2184c81e510fcde72316c0a69280a2b6c62bdf21e90ab4debf445/neurokit2-0.1.4.1-py2.py3-none-any.whl",
    )
    version(
        "0.1.2",
        sha256="72baa7bd15a265a6e2cf6e9e4f4c9bc525605b9ec16c10e51ce84a701faf446b",
        url="https://pypi.org/packages/7c/ff/960c5e878b192921b8aad7bbc0be485e77da368c0215b5cb79e8e689beb3/neurokit2-0.1.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-matplotlib")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-scikit-learn@1.0:", when="@0.2:")
        depends_on("py-scikit-learn", when="@0.1")
        depends_on("py-scipy")
