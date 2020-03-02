# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# The following statements are needed to support subprocess code coverage
try:
    import coverage
    coverage.process_startup()
except Exception:
    pass
