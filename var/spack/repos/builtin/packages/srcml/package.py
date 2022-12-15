# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Srcml(CMakePackage):
    """srcML is an XML format for source code. The XML markup identifies elements of
    the abstract syntax of the source-code language. The toolkit includes parsing
    supports conversion of C, C++, C#, and Java both to and from the srcML format.
    The format allows leveraging XML tools to support the various tasks of source
    code exploration, analysis, and manipulation."""

    homepage = "https://github.com/srcML/srcML"
    url      = "https://github.com/srcML/srcML/archive/refs/tags/v1.0.0.tar.gz"

    maintainers = ["meyersbs"]

    version("1.0.0", sha256="3ddf33271c3b3953d5e3ecbb14c4f925fc0e609a81250d921d3516537dcffae2")

    # From https://github.com/srcML/Docker/blob/centos_latest/base/Dockerfile:
    depends_on("which",       type=("build", "run"))
    depends_on("zip",         type=("build", "run"))
    depends_on("unzip",       type=("build", "run"))
    depends_on("gcc",         type=("build", "run"))
    depends_on("cmake@3.14:", type=("build", "run"))
    depends_on("antlr",       type=("build", "run"))
    depends_on("antlr+cxx",   type=("build", "run"))
    depends_on("libxml2",     type=("build", "run"))  ## Missing +devel
    depends_on("libxslt",     type=("build", "run"))  ## Missing +devel
    depends_on("libarchive",  type=("build", "run"))  ## Missing +devel
    depends_on("openssl",     type=("build", "run"))  ## Missing +devel
    depends_on("curl",        type=("build", "run"))  ## Missing +devel
    depends_on("bzip2",       type=("build", "run"))
    depends_on("ninja",       type=("build", "run"))
    # From build errors:
    depends_on("boost",       type=("build", "run"))
