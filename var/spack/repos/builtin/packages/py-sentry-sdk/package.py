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

    variant("aiohttp", default=False, description="Builts with aiohttp")
    variant("beam", default=False, description="Builts with beam")
    variant("bottle", default=False, description="Builts with bottle")
    variant("celery", default=False, description="Builts with celery")
    variant("chalice", default=False, description="Builts with chalice")
    variant("django", default=False, description="Builts with django")
    variant("falcon", default=False, description="Builts with falcon")
    variant("flask", default=False, description="Builts with flask")
    variant("httpx", default=False, when="@1.5.5:", description="Builts with httpx")
    variant("pure_eval", default=False, description="Builts with pure_eval")
    variant("pyspark", default=False, description="Builts with pyspark")
    variant("quart", default=False, when="@1.5.5:", description="Builts with quart")
    variant("rq", default=False, description="Builts with rq")
    variant("sanic", default=False, description="Builts with sanic")
    variant("sqlalchemy", default=False, description="Builts with sqlalchemy")
    variant("tornado", default=False, description="Builts with tornado")

    with default_args(type="run"):
        depends_on("py-aiohttp@3.5.0:", when="@:0.20.0,0.20.2:+aiohttp")
        depends_on("py-apache-beam@2.12:", when="@:0.20.0,0.20.2:+beam")
        depends_on("py-blinker@1.1:", when="@1.5.2:+quart")
        depends_on("py-blinker@1.1:", when="@:0.20.0,0.20.2:+flask")
        depends_on("py-bottle@0.12.13:", when="@:0.20.0,0.20.2:+bottle")
        depends_on("py-celery@3:", when="@:0.20.0,0.20.2:+celery")
        depends_on("py-certifi", when="@:0.20.0,0.20.2:")
        depends_on("py-chalice@1.16:", when="@0.17.4:0.20.0,0.20.2:+chalice")
        depends_on("py-django@1.8:", when="@:0.20.0,0.20.2:+django")
        depends_on("py-falcon@1.4.0:", when="@:0.20.0,0.20.2:+falcon")
        depends_on("py-flask@0.11:", when="@:0.20.0,0.20.2:1.5.8,1.5.10:+flask")
        depends_on("py-httpx@0.16:", when="@1.2:+httpx")
        depends_on("py-pyspark@2.4.4:", when="@:0.20.0,0.20.2:+pyspark")
        depends_on("py-quart@0.16.1:", when="@1.5.2:+quart")
        depends_on("py-rq@0.6:", when="@:0.20.0,0.20.2:+rq")
        depends_on("py-sanic@0.8:", when="@:0.20.0,0.20.2:+sanic")
        depends_on("py-sqlalchemy@1.2.0:", when="@:0.20.0,0.20.2:+sqlalchemy")
        depends_on("py-tornado@5.0:", when="@:0.20.0,0.20.2:+tornado")
        depends_on("py-urllib3@1.10:", when="@:0.20.0,0.20.2:1.9.0")
