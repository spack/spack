# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class TransitiveConditionalVirtualDependency(BundlePackage):
    """Depends on a package with a conditional virtual dependency."""
    homepage = "https://dev.null"

    version('1.0')
    depends_on('conditional-virtual-dependency')
