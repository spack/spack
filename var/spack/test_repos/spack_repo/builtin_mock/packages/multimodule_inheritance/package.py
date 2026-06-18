# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ..simple_inheritance import package as si


class MultimoduleInheritance(si.BaseWithDirectives):
    """Simple package which inherits a method and several directives"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/multimodule-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("openblas", when="+openblas")
