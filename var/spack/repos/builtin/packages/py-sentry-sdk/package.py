# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySentrySdk(PythonPackage):
    """The new Python SDK for Sentry.io"""

    homepage = "https://github.com/getsentry/sentry-python"
    pypi = "sentry-sdk/sentry-sdk-0.17.6.tar.gz"

    license("MIT")

    version(
        "1.5.5",
        sha256="3817274fba2498c8ebf6b896ee98ac916c5598706340573268c07bf2bb30d831",
        url="https://pypi.org/packages/3f/6a/01fb4e5417f5d2ef6279883a9deedabb6b6f223aa706892ea9caa6d7c1e4/sentry_sdk-1.5.5-py2.py3-none-any.whl",
    )
    version(
        "0.17.6",
        sha256="45486deb031cea6bbb25a540d7adb4dd48cd8a1cc31e6a5ce9fb4f792a572e9a",
        url="https://pypi.org/packages/c8/6c/6dcf4f21bec0b0d0685b4992ee414506342b09267e4a2ab24472625f9d8d/sentry_sdk-0.17.6-py2.py3-none-any.whl",
    )

    variant("aiohttp", default=False)
    variant("beam", default=False)
    variant("bottle", default=False)
    variant("celery", default=False)
    variant("chalice", default=False)
    variant("django", default=False)
    variant("falcon", default=False)
    variant("flask", default=False)
    variant("httpx", default=False)
    variant("pure_eval", default=False)
    variant("pyspark", default=False)
    variant("quart", default=False)
    variant("rq", default=False)
    variant("sanic", default=False)
    variant("sqlalchemy", default=False)
    variant("tornado", default=False)

    with default_args(type="run"):
        depends_on("py-aiohttp@3.5.0:", when="@0.15:0.20.0,0.20.2:+aiohttp")
        depends_on("py-apache-beam@2.12:", when="@0.16:0.20.0,0.20.2:+beam")
        depends_on("py-blinker@1.1:", when="@1.5.2:+quart")
        depends_on(
            "py-blinker@1.1:",
            when="@:0.1.0-rc1,0.1.0-rc3,0.1.0-rc5:0.1.0-rc6,0.1.0-rc11,0.1.0-rc14,"
            "0.1.0-rc16:0.1.0,0.1.2,0.4:0.4.0,0.5:0.5.1,0.5.4,0.6:0.6.1,0.6.6,0.6.8:0.7.0,"
            "0.7.3,0.7.12,0.7.14:0.7,0.8.1:0.8,0.12:0.12.2,0.13.1,0.15:0.20.0,0.20.2:+flask",
        )
        depends_on(
            "py-bottle@0.12.13:",
            when="@0.7.12,0.7.14:0.7,0.8.1:0.8,0.12:0.12.2,0.13.1,0.15:0.20.0,0.20.2:+bottle",
        )
        depends_on("py-celery@3:", when="@0.15:0.20.0,0.20.2:+celery")
        depends_on(
            "py-certifi",
            when="@:0.1.0-rc1,0.1.0-rc3,0.1.0-rc5:0.1.0-rc6,0.1.0-rc11,0.1.0-rc14,"
            "0.1.0-rc16:0.1.0,0.1.2,0.4:0.4.0,0.5:0.5.1,0.5.4,0.6:0.6.1,0.6.6,0.6.8:0.7.0,"
            "0.7.3,0.7.12,0.7.14:0.7,0.8.1:0.8,0.12:0.12.2,0.13.1,0.15:0.20.0,0.20.2:",
        )
        depends_on("py-chalice@1.16:", when="@0.17.4:0.20.0,0.20.2:+chalice")
        depends_on("py-django@1.8:", when="@0.15:0.20.0,0.20.2:+django")
        depends_on(
            "py-falcon@1.4.0:",
            when="@0.7.12,0.7.14:0.7,0.8.1:0.8,0.12:0.12.2,0.13.1,0.15:0.20.0,0.20.2:+falcon",
        )
        depends_on("py-flask@0.11:", when="@0.15:0.20.0,0.20.2:1.5.8,1.5.10:+flask")
        depends_on("py-httpx@0.16:", when="@1.2:+httpx")
        depends_on("py-pyspark@2.4.4:", when="@0.15:0.20.0,0.20.2:+pyspark")
        depends_on("py-quart@0.16.1:", when="@1.5.2:+quart")
        depends_on("py-rq@0.6:", when="@0.15:0.20.0,0.20.2:+rq")
        depends_on("py-sanic@0.8:", when="@0.15:0.20.0,0.20.2:+sanic")
        depends_on("py-sqlalchemy@1.2.0:", when="@0.15:0.20.0,0.20.2:+sqlalchemy")
        depends_on("py-tornado@5.0:", when="@0.15:0.20.0,0.20.2:+tornado")
        depends_on("py-urllib3@1.10:", when="@0.13.1,0.15:0.20.0,0.20.2:1.9.0")
