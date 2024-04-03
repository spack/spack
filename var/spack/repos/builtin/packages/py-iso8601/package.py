# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIso8601(PythonPackage):
    """Simple module to parse ISO 8601 dates"""

    homepage = "https://github.com/micktwomey/pyiso8601"
    pypi = "iso8601/iso8601-0.1.14.tar.gz"

    license("MIT")

    version(
        "1.1.0",
        sha256="8400e90141bf792bce2634df533dc57e3bee19ea120a87bebcd3da89a58ad73f",
        url="https://pypi.org/packages/65/6c/9d72435c72adfa6e4ed1824b6df7fffbeaaf15c653881e9b041a318ba572/iso8601-1.1.0-py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="d7bc01b1c2a43b259570bb307f057abc578786ea734ba2b87b836c5efc5bd443",
        url="https://pypi.org/packages/df/e5/589bc81d410139ec4e4f37d9af5a50987566abf6d087b3c4fbed708109a9/iso8601-1.0.2-py3-none-any.whl",
    )
    version(
        "0.1.14",
        sha256="e7e1122f064d626e17d47cd5106bed2c620cb38fe464999e0ddae2b6d2de6004",
        url="https://pypi.org/packages/c5/10/da48dc228b821a64407c2527e1e8ee98917b36e80a181f2ca06ea3cb676b/iso8601-0.1.14-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@1")
