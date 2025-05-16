# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from ..variant_values.package import VariantValues


class VariantValuesOverride(VariantValues):
    """Test variant value validation with multiple definitions."""

    variant("v", default="baz", values=["bar", "baz"])
