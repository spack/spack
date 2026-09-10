# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Allow running spack as ``python -m spack``."""

import sys

from spack.main import main

if __name__ == "__main__":
    sys.exit(main())
