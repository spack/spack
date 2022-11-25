# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snakemake(PythonPackage):
    """Snakemake is an MIT-licensed workflow management system."""

    homepage = "https://snakemake.readthedocs.io/en/stable/"
    pypi = "snakemake/snakemake-6.12.3.tar.gz"
    maintainers = ["marcusboden"]

    version("7.18.2", sha256="23f52b9a0c86da3b974a3cfc097fa82b41c49dab05543c0d18377c854852f771")
    version("6.15.1", sha256="a219601d57037f565ead9963e6bd8d04d3bdd985d172371e54197dcbdba79865")
    version("6.13.1", sha256="22f57dcd8b1ca8a30aaa45c5d2c0f56d381d4731abd0988f24f9de46b7d9827c")
    version("6.12.3", sha256="af86af9a540da3dceb05dad1040f1d3d733e6a695f8b3f8c30f8cf3bc6570a88")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools@42:", type=("build", "run"), when="@7:")

    # See https://github.com/snakemake/snakemake/blob/v7.18.2/setup.py#L56
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-throttler", type=("build", "run"), when="@7:")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-configargparse", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-datrie", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-toposort", type=("build", "run"))
    depends_on("py-connectionpool@0.0.3:", type=("build", "run"))
    depends_on("py-pulp@2:", type=("build", "run"))
    depends_on("py-smart-open@3:", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"), when="@:6")
    depends_on("py-stopit", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-ratelimiter", type=("build", "run"), when="@:6")
    depends_on("py-yte@1", type=("build", "run"), when="@7:")
    depends_on("py-jinja2@3", type=("build", "run"), when="@7:")
    depends_on("py-reretry", type=("build", "run"), when="@7:")

    variant("reports", default=False, description="Generate self-contained HTML reports")
    with when("+reports"):
        depends_on("py-jinja2", type=("build", "run"))
        depends_on("py-networkx", type=("build", "run"))
        depends_on("py-pygments", type=("build", "run"))
        depends_on("py-pygraphviz", type=("build", "run"))

    variant("google-cloud", default=False, description="Enable Google Cloud execution")
    with when("+google-cloud"):
        depends_on("py-oauth2client", type=("build", "run"))
        depends_on("py-google-crc32c", type=("build", "run"))
        depends_on("py-google-api-python-client", type=("build", "run"))
        depends_on("py-google-cloud-storage", type=("build", "run"))

    # These variants are not in PyPI/pip, but they are undocumented dependencies
    # needed to make certain parts of Snakemake work.
    variant("ftp", default=False, description="Enable snakemake.remote.FTP")
    depends_on("py-ftputil", when="+ftp")

    variant("s3", default=False, description="Enable snakemake.remote.S3")
    depends_on("py-boto3", when="+s3")
    depends_on("py-botocore", when="+s3")

    variant("http", default=False, description="Enable snakemake.remote.HTTP")
    depends_on("py-requests", when="+http")

    def test(self):
        Executable("snakemake")("--version")
