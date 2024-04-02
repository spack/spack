# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyElasticsearch(PythonPackage):
    """Python client for Elasticsearch"""

    homepage = "https://github.com/elastic/elasticsearch-py"
    pypi = "elasticsearch/elasticsearch-5.2.0.tar.gz"

    license("Apache-2.0")

    version(
        "8.6.2",
        sha256="8ccbebd9a0f6f523c7db67bb54863dde8bdb93daae4ff97f7c814e0500a73e84",
        url="https://pypi.org/packages/f7/43/f73f5a5cc40b1943f90a895b248a4985a4b23aa25439d7919bc6ab147398/elasticsearch-8.6.2-py3-none-any.whl",
    )
    version(
        "7.6.0",
        sha256="f4bb05cfe55cf369bdcb4d86d0129d39d66a91fd9517b13cd4e4231fbfcf5c81",
        url="https://pypi.org/packages/cc/cf/7973ac58090b960857da04add0b345415bf1e1741beddf4cbe136b8ad174/elasticsearch-7.6.0-py2.py3-none-any.whl",
    )
    version(
        "7.5.1",
        sha256="1815ee1377e7d3cf32770738a70785fe4ab1f05be28336a330ed71cb295a7c6c",
        url="https://pypi.org/packages/10/60/0c79dde3e81beffeed422599d9ac65419289095186d37a3201739d52a57d/elasticsearch-7.5.1-py2.py3-none-any.whl",
    )
    version(
        "6.4.0",
        sha256="1f0f633e3b500d5042424f75a505badf8c4b9962c1b4734cdfb3087fb67920be",
        url="https://pypi.org/packages/e0/b3/14dd62dfee3b0bca512167edc6f8baf5149b1108a02f9f246021953d117c/elasticsearch-6.4.0-py2.py3-none-any.whl",
    )
    version(
        "5.2.0",
        sha256="db1a1000308db56f1475e059d28238238fafc20aab8cbf0ec0c3011f1caecd65",
        url="https://pypi.org/packages/44/e8/3529a15f3ccf9200fc2d8832b2aaa886a09b2086bb5232ffb9dd3209e4ff/elasticsearch-5.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="6f184507c151bf8b093b86c0b7cd576a1d730acee03e8213cae367f196ad4c5c",
        url="https://pypi.org/packages/c3/db/3869181ba938814d092a53ffbe2597be8597f0a4be62fc3989a82b0fa85a/elasticsearch-2.3.0-py2.py3-none-any.whl",
    )

    variant("async", when="@8.6.2:", default=False, description="Include support for asyncio")

    with default_args(type="run"):
        depends_on("python@:3", when="@6.8:6,7.6:8.10")
        depends_on("py-aiohttp@3.0.0:3", when="@7.8:+async")
        depends_on("py-elastic-transport@8.0.0:", when="@8.0.0:8.12")
        depends_on("py-urllib3@1.21.1:", when="@6.8:6,7.6:7.9")

    # tests_require
    # depends_on('py-requests@1.0.0:2.9', type=('build', 'run'))
    # depends_on('py-nose', type=('build', 'run'))
    # depends_on('py-coverage', type=('build', 'run'))
    # depends_on('py-mock', type=('build', 'run'))
    # depends_on('py-pyyaml', type=('build', 'run'))
    # depends_on('py-nosexcover', type=('build', 'run'))
