# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThreadpoolctl(PythonPackage):
    """Python helpers to limit the number of threads used in the
    threadpool-backed of common native libraries used for scientific
    computing and data science (e.g. BLAS and OpenMP)."""

    homepage = "https://github.com/joblib/threadpoolctl"
    pypi = "threadpoolctl/threadpoolctl-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.1.0",
        sha256="8b99adda265feb6773280df41eece7b2e6561b772d21ffd52e372f999024907b",
        url="https://pypi.org/packages/61/cf/6e354304bcb9c6413c4e02a747b600061c21d38ba51e7e544ac7bc66aecc/threadpoolctl-3.1.0-py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="4fade5b3b48ae4b1c30f200b28f39180371104fccc642e039e0f2435ec8cc211",
        url="https://pypi.org/packages/ff/fe/8aaca2a0db7fd80f0b2cf8a16a034d3eea8102d58ff9331d2aaf1f06766a/threadpoolctl-3.0.0-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="72eed211bb25feecc3244c5c26b015579777a466589e9b854c66f18d6deaeee1",
        url="https://pypi.org/packages/db/09/cab2f398e28e9f183714afde872b2ce23629f5833e467b151f18e1e08908/threadpoolctl-2.0.0-py3-none-any.whl",
    )
