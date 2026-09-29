# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Registered here rather than in lib/spack/spack/test/conftest.py because pytest 7.0.1 -- the
# latest pytest supporting the oldest Python we test (3.6) -- rejects pytest_plugins in a
# non-top-level conftest.
pytest_plugins = ["spack.test.concretization_cache_plugin"]
