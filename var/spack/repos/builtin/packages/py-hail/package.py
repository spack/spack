# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-hail
#
# You can edit this file again by typing:
#
#     spack edit py-hail
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyHail(PythonPackage):
    """Cloud-native genomic dataframes and batch computing (Python API)"""

    homepage = "https://hail.is"
    pypi = "hail/hail-0.2.130-py3-none-any.whl"

    maintainers("teaguesterling")

    license("MIT", checked_by="teaguesterling")

    version(
        "0.2.130",
        sha256="c0f1f3ae52406a13eecb44ebe445be7d677d2c3b4e4e29269ecb53b7ac55168e",
        expand=False
    )

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")

    # HAIL API requirements
    with default_args(type=("build", "run")):
        depends_on("py-avro@1.10:1.11")
        depends_on("py-bokeh@:3.3")
        depends_on("py-decorator@:4.4.2")
        depends_on("py-deprecated@1.2.10:1.2")
        depends_on("py-numpy@:2")
        depends_on("py-pandas@2")
        depends_on("py-parsimonious@:0")
        depends_on("py-plotly@5.18:5.20")
        depends_on("py-protobuf@3.20.2")
        depends_on("py-requests@2.31")
        depends_on("py-scipy@1.3:1.11")

    # HAIL wheels are pinned to a specific version of
    # Spark. If we implement building from source, this
    # will likely not be as much of an issue, but that
    # isn't working yet.
    with default_args(type=("build", "run")):
        depends_on("py-pyspark@3.3", when="@0.2.130")

    # hailtop requirements
    with default_args(type=("build", "run")):
        depends_on("py-aiodns@2")
        depends_on("py-aiohttp@3.9")
        depends_on("py-azure-identity@1.6:1")
        depends_on("py-azure-mgmt-storage@20.1.0")
        depends_on("py-azure-storage-blob@12.11:12")
        depends_on("py-boto3@1.17:1")
        depends_on("py-botocore@1.20:1")
        depends_on("py-dill@0.3.6:0.3")
        depends_on("py-frozenlist@1.3.1:1")
        depends_on("py-google-auth@2.14.1:2")
        depends_on("py-google-auth-oauthlib@0.5.2:0")
        depends_on("py-humanize@1.0.0:1")
        depends_on("py-janus@0.6:1.0")
        depends_on("py-nest-asyncio@1.5.8:1")
        depends_on("py-rich@12.6.0:12")
        depends_on("py-orjson@3.9.15:3")
        depends_on("py-typer@0.9.0:0")
        depends_on("py-python-json-logger@2.0.2:2")
        depends_on("py-pyyaml@6.0:7")
        depends_on("py-sortedcontainers@2.4.0:2")
        depends_on("py-tabulate@0.8.9:0")
        depends_on("py-uvloop@0.19.0:0")
        depends_on("py-jproperties@2.1.1:2")

    # Undocumented runtime requirements for hailtop
    # These are also required to use the HAIL API
    # but are not explicitly mentioned anywhere
    with default_args(type="run"):
        depends_on("py-azure-mgmt-core")
        depends_on("py-typing-extensions")

