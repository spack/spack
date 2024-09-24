# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGssapiGsi(AutotoolsPackage):
    """The Grid Security Infrastructure, an implementation of an authentication
    and authorization infrastructure based upon the concept of X509 proxy
    certificates. The GSI packages include client and server code necessary
    to create and verify proxies."""

    homepage = "https://github.com/gridcf/gct/tree/master/gsi/gssapi/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gssapi_gsi-14.20.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("14.20", sha256="2ba4e905f1dbbbee8ade01a6d0d59a9b5e816620fe5b080de0524b5331614236")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("awk", type="build")

    depends_on("openssl")

    depends_on("globus-common")
