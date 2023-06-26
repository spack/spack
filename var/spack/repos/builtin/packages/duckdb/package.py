# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Duckdb(CMakePackage):
    """DuckDB is an in-process SQL OLAP Database Management System."""

    homepage = "https://duckdb.org"
    url = "https://github.com/duckdb/duckdb/archive/refs/tags/v0.7.1.tar.gz"
    git = "https://github.com/duckdb/duckdb.git"

    version("master", branch="master")
    version("0.7.1", sha256="67f840f861e5ffbe137d65a8543642d016f900b89dd035492d562ad11acf0e1e")
