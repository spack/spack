# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLlnlSina(PythonPackage):
    """Sina allows codes to store, query, and visualize their data through an
    easy-to-use Python API. Data that fits its recognized schema can be ingested
    into one or more supported backends.
    Sina's API is independent of backend and gives users the benefits of a database
    without requiring knowledge of one, allowing queries to be expressed in pure
    Python.  Visualizations are also provided through Python.

    Sina is intended especially for use with run metadata,
    allowing users to easily and efficiently find simulation runs that match some
    criteria.
    """

    homepage = "https://github.com/LLNL/Sina"
    git = "https://github.com/LLNL/Sina.git"

    # notify when the package is updated.

    license("MIT")

    maintainers("HaluskaR", "estebanpauli", "murray55", "doutriaux1")
    version(
        "1.11.0",
        sha256="a9891e8b050df40c5145d53eb5daf7ee622854a0e26876e1643463d6665f561e",
        url="https://pypi.org/packages/f1/f7/3b3ec3791e5b0198a195a57b427473801e0f8776e23307fc5b6b95a6c5b9/llnl_sina-1.11.0-py2.py3-none-any.whl",
    )
    version(
        "1.10.0",
        sha256="70b84738d1ae2a1bda988c1b508c5e32867ce75b5460fce5d5e941e377e6d0a5",
        url="https://pypi.org/packages/39/d9/faf441dcaba99567f8804516f0faf37de726d4cc65b5f1454153ddec615e/llnl_sina-1.10.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six")
        depends_on("py-sqlalchemy", when="@:1.13")

    # let's remove dependency on orjson

    build_directory = "python"
