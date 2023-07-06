# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.paths
from spack.package import *


class UrlListTest(Package):
    """Mock package with url_list."""

    homepage = "http://www.url-list-example.com"

    web_data_path = join_path(spack.paths.test_path, "data", "web")
    url = "file://" + web_data_path + "/foo-0.0.0.tar.gz"
    list_url = "file://" + web_data_path + "/index.html"
    list_depth = 3

    version("0.0.0", md5="00000000000000000000000000000000")
    version("1.0.0", md5="00000000000000000000000000000100")
    version("3.0", md5="00000000000000000000000000000030")
    version("4.5", md5="00000000000000000000000000000450")
    version("2.0.0b2", md5="000000000000000000000000000200b2")
    version("3.0a1", md5="000000000000000000000000000030a1")
    version("4.5-rc5", md5="000000000000000000000000000045c5")
