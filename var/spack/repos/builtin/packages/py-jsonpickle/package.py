# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyJsonpickle(PythonPackage):
    """Python library for serializing any arbitrary object graph into JSON."""

    homepage = "https://github.com/jsonpickle/jsonpickle"
    pypi = "jsonpickle/jsonpickle-1.4.1.tar.gz"

    version('2.0.0', sha256='0be49cba80ea6f87a168aa8168d717d00c6ca07ba83df3cec32d3b30bfe6fb9a')
    version('1.5.2', sha256='9e899bcf94bb1ce6e17beccf880d096fd6221681faede55aa7a8349556822359')
    version('1.5.1', sha256='060f97096559d1b86aa16cac2f4ea5f7b6da0c15d8a4de150b78013a886f9a51')
    version('1.5.0', sha256='1bd34a2ae8e51d3adbcafe83dc2d5cc81be53ada8bb16959ca6aca499bceada2')
    version('1.4.2', sha256='c9b99b28a9e6a3043ec993552db79f4389da11afcb1d0246d93c79f4b5e64062')
    version('1.4.1', sha256='e8d4b7cd0bd6826001a74377df1079a76ad8bae0f909282de2554164c837c8ba')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@3.4.1:+toml', type='build')
    depends_on('py-importlib-metadata', type=('build', 'run'))
