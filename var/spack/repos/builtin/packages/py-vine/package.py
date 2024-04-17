# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVine(PythonPackage):
    """Promises, promises, promises."""

    pypi = "vine/vine-1.2.0.tar.gz"

    license("CC-BY-SA-4.0")

    version(
        "5.1.0",
        sha256="40fdf3c48b2cfe1c38a49e9ae2da6fda88e4794c810050a728bd7413811fb1dc",
        url="https://pypi.org/packages/03/ff/7c0c86c43b3cbb927e0ccc0255cb4057ceba4799cd44ae95174ce8e8b5b2/vine-5.1.0-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="4c9dceab6f76ed92105027c49c823800dd33cacce13bdedc5b914e3514b7fb30",
        url="https://pypi.org/packages/8d/61/a7badb48186919a9fd7cf0ef427cab6d16e0ed474035c36fa64ddd72bfa2/vine-5.0.0-py2.py3-none-any.whl",
    )
    version(
        "5.0.0-alpha1",
        sha256="971dfaa5e6039bd8fb5a96b9e4f15f792c1acfdc26fd69ef8b36149812194e32",
        url="https://pypi.org/packages/eb/cd/df502a2e7cb4050e46ac674195ca780164df6b822baca40374f0bfbee61e/vine-5.0.0a1-py2.py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="ea4947cc56d1fd6f2095c8d543ee25dad966f78692528e68b4fada11ba3f98af",
        url="https://pypi.org/packages/7f/60/82c03047396126c8331ceb64da1dc52d4f1317209f32e8fe286d0c07365a/vine-1.3.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="3cd505dcf980223cfaf13423d371f2e7ff99247e38d5985a01ec8264e4f2aca1",
        url="https://pypi.org/packages/62/dd/e30f828a39914626d67876b987d6fc47616b64de680cd0f746fc9c8aab47/vine-1.2.0-py2.py3-none-any.whl",
    )
