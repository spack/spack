# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySeriate(PythonPackage):
    """This is a Python implementation of Seriation
    algorithm. Seriation is an approach for ordering elements in a set
    so that the sum of the sequential pairwise distances is
    minimal. We state this task as a Travelling Salesman Problem (TSP)
    and leverage the powerful Google's or-tools to do
    heavy-lifting. Since TSP is NP-hard, it is not possible to
    calculate the precise solution for a big number of
    elements. However, the or-tools' heuristics work very well in
    practice, and they are used in e.g. Google Maps."""

    homepage = "https://github.com/src-d/seriate"
    url = "https://github.com/src-d/seriate/archive/1.1.2.tar.gz"

    license("Apache-2.0")

    version(
        "1.1.2",
        sha256="f813ae54214dec4ab689cade548cdedeae28fce19fec598f5f3c3415787b4dc1",
        url="https://pypi.org/packages/6a/dd/c2343154d01e0062d464ec083488417134ca9b891d067822a1e770a57c98/seriate-1.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-ortools@6.7.4973:7", when="@1.0.1:")
        depends_on("py-packaging@16:", when="@1.0.1:")
