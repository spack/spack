# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMaestrowf(PythonPackage):
    """A general purpose workflow conductor for running multi-step
    simulation studies."""

    homepage = "https://github.com/LLNL/maestrowf/"
    pypi = "maestrowf/maestrowf-1.1.8.tar.gz"
    git = "https://github.com/LLNL/maestrowf/"
    tags = ["radiuss"]

    maintainers("FrankD412")

    license("MIT")

    # git branches
    version(
        "1.1.9",
        sha256="2693364873ac21e8854d08bacb08378b527f4b691cdbdaae5872d30d850ff855",
        url="https://pypi.org/packages/47/05/a13794cd893536a97e953500691398678c3adb0f456c97bc5c93ed379af8/maestrowf-1.1.9-py3-none-any.whl",
    )
    version(
        "1.1.8",
        sha256="a5ef26c79fff0ef027e0033fdf079aa53abeb953014733baf7833908185e8157",
        url="https://pypi.org/packages/a0/fe/64b2e4256a04adf66a4f6caf21cf30d5b37d1abbd2e9423a35019eb8cab7/maestrowf-1.1.8-py2.py3-none-any.whl",
    )
    version(
        "1.1.7",
        sha256="0c6ad3cc3d34944d68f47fe7c7d4ed8dd1e73bfb566adc9a3e0f67cfcf7fcda7",
        url="https://pypi.org/packages/9a/ab/de90982bddacf9d4521d4bda787d4f394c8648534b1c9aff9c2d9c5bdb1a/maestrowf-1.1.7-py2.py3-none-any.whl",
    )
    version(
        "1.1.6",
        sha256="3960dad32f6a603ce9c47ea1bce64cfddf7f6f4e135346336e83e4945c4f4524",
        url="https://pypi.org/packages/49/3a/a7b75e05e5b615072f392dd567951bdb001a887b4b67f0c92396665bb579/maestrowf-1.1.6-py2.py3-none-any.whl",
    )
    version(
        "1.1.4",
        sha256="c74b4ff0718f86ecac69c98811f991d87c67e89736009435e37bc6cfcd669448",
        url="https://pypi.org/packages/d1/82/f2dbdf98f7730bb06095157bb0243c4895310288b61aed6b9836d786fc61/maestrowf-1.1.4-py2.py3-none-any.whl",
    )
    version(
        "1.1.3",
        sha256="0ce3f6f1473da1b1069f87ee95b0addb84dd0b2c742fe0bbae8cfec6ecd1cf0f",
        url="https://pypi.org/packages/7e/02/621a00b84a74fcd060cfca2b17fb66a8feb5cdda6ca9fb68d91d2d44d259/maestrowf-1.1.3-py2.py3-none-any.whl",
    )
    version(
        "1.1.2",
        sha256="b372543fd01a15d495f318f08a689c8bd7656d54dbd437558d1fe34178c536ea",
        url="https://pypi.org/packages/2f/7f/8911e2c964f0ce4740cc614ddd8c32cd701c214f7bab4d5c28ac1709049f/maestrowf-1.1.2-py2.py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="072fa07b5e23b23ff95c389d707b99262868599e22a44d7ef7f48fd59c0b257e",
        url="https://pypi.org/packages/7b/ce/7e5aec5eb28cf1638d855324d14047bed2f4d1a4d6f722cc88d297457ee7/maestrowf-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="dd5ec9c1a6a4ce62049f5934bd016c80d79197aa73dbc7205524cc8d6ea7fcfc",
        url="https://pypi.org/packages/bb/43/5c9c9af3cc5abba7f16cad3f972209a06043a1a3a778a131062098e7bdf6/maestrowf-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="cc1a6060ce74f7f01aa9755d432c98f0146ad24d8d487993f0e4feaf436866f8",
        url="https://pypi.org/packages/9b/31/1d58cfc5cfb9ca9225fb9fae77fa531bcfe9506c23edc001d2d8fe93d90e/maestrowf-1.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-coloredlogs", when="@1.1.7:1.1.7.0,1.1.8:")
        depends_on("py-dill", when="@1.1.7:1.1.7.0,1.1.8:")
        depends_on("py-enum34", when="@:1.1.3")
        depends_on("py-filelock", when="@1.1:")
        depends_on("py-jsonschema@3.2:", when="@1.1.7:1.1.7.0,1.1.8:")
        depends_on("py-pyyaml@4:", when="@1.1.4:")
        depends_on("py-pyyaml", when="@:1.1.3")
        depends_on("py-rich", when="@1.1.9:")
        depends_on("py-six")
        depends_on("py-tabulate", when="@1.1:")

    # pypi releases
