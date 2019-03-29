# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MariadbConnectorC(CMakePackage):
    """MariaDB Connector/C is used to connect applications
       developed in C/C++ to MariaDB and MySQL databases."""

    homepage = "https://downloads.mariadb.org/connector-c/"
    url      = "https://downloads.mariadb.org/f/connector-c-3.0.9/mariadb-connector-c-3.0.9-src.tar.gz"

    version('3.0.9', sha256='7277c0caba6f50b1d07e1d682baf0b962a63e2e6af9e00e09b8dcf36a7858641')
