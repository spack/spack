# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snakemake(PythonPackage):
    """Snakemake is an MIT-licensed workflow management system."""

    homepage = "https://snakemake.readthedocs.io/en/stable/"
    pypi = "snakemake/snakemake-6.12.3.tar.gz"
    maintainers("marcusboden")

    version("7.22.0", sha256="68d7bb4ab7555f7b58a3ba748a880024df919042cfb670da231886385de697cd")
    version("7.21.0", sha256="ebf91f4ca5c70809fcbfd2e8cbc982096cdadac1ec34138bb147b4a8c975c85b")
    version("7.20.0", sha256="f5b45191f1d419ebf28606880cb9bfac3bfa7c5949d1d2b64f551586d4212a2a")
    version("7.19.1", sha256="390ad5e2d5106e84700b7219c0eddf41d61be2205787d77a815fa91e4d624f33")
    version("7.19.0", sha256="423bb6f10013d874b6b71c06cbb45b2935ce1a291f74e1fc1614efa44b08c3e7")
    version("7.18.2", sha256="23f52b9a0c86da3b974a3cfc097fa82b41c49dab05543c0d18377c854852f771")
    version("6.15.1", sha256="a219601d57037f565ead9963e6bd8d04d3bdd985d172371e54197dcbdba79865")
    version("6.13.1", sha256="22f57dcd8b1ca8a30aaa45c5d2c0f56d381d4731abd0988f24f9de46b7d9827c")
    version("6.12.3", sha256="af86af9a540da3dceb05dad1040f1d3d733e6a695f8b3f8c30f8cf3bc6570a88")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools@42:", type=("build", "run"), when="@7:")

    # See https://github.com/snakemake/snakemake/pull/2065
    depends_on("py-tomli", type=("build"), when="@7.20.0: ^python@:3.10")
    # See https://github.com/snakemake/snakemake/blob/v7.20.0/setup.cfg#L44
    depends_on("py-humanfriendly", type=("build", "run"), when="@7.20.0:")
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
        depends_on("py-jinja2", type=("build", "run"), when="@:7.19.1")
        depends_on("py-pygments", type=("build", "run"))
        # https://github.com/snakemake/snakemake/pull/1470
        depends_on("py-networkx", type=("build", "run"), when="@:7.1.1")
        depends_on("py-pygraphviz", type=("build", "run"), when="@:7.1.1")

    variant("google-cloud", default=False, description="Enable Google Cloud execution")
    with when("+google-cloud"):
        depends_on("py-oauth2client", type=("build", "run"))
        depends_on("py-google-crc32c", type=("build", "run"))
        depends_on("py-google-api-python-client", type=("build", "run"))
        depends_on("py-google-cloud-storage", type=("build", "run"))

    # These variants are not in PyPI/pip, but they are undocumented dependencies
    # needed to make certain parts of Snakemake work.
    variant("ftp", default=False, description="Enable snakemake.remote.FTP")
    depends_on("py-ftputil", when="+ftp", type=("build", "run"))

    variant("s3", default=False, description="Enable snakemake.remote.S3")
    depends_on("py-boto3", when="+s3", type=("build", "run"))
    depends_on("py-botocore", when="+s3", type=("build", "run"))

    variant("http", default=False, description="Enable snakemake.remote.HTTP")
    depends_on("py-requests", when="+http", type=("build", "run"))

    def test(self):
        Executable("snakemake")("--version")
