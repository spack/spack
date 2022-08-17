# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRuamelYamlClib(PythonPackage):
    """C version of reader, parser and emitter for ruamel.yaml derived from
    libyaml."""

    homepage = "https://sourceforge.net/p/ruamel-yaml-clib/code/ci/default/tree/"
    pypi = "ruamel.yaml.clib/ruamel.yaml.clib-0.2.0.tar.gz"

    version("0.2.4", sha256="f997f13fd94e37e8b7d7dbe759088bb428adc6570da06b64a913d932d891ac8d")
    version("0.2.0", sha256="b66832ea8077d9b3f6e311c4a53d06273db5dc2db6e8a908550f3c14d67e718c")

    # https://sourceforge.net/p/ruamel-yaml-clib/tickets/5
    depends_on("python@2.7:2.8,3.5:3.9", when="@:0.2.1", type=("build", "link", "run"))
    depends_on("python@3.5:",            when="@0.2.4:", type=("build", "link", "run"))
    depends_on("py-setuptools@28.7.0:", type="build")
