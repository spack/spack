# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builder_test.packages.callbacks import package as callbacks


class InheritanceOnlyPackage(callbacks.Callbacks):
    """Package used to verify that inheritance among packages works as expected,
    when there is no override of the builder class.
    """

    pass
