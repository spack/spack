# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REstimability(RPackage):
    """Tools for Assessing Estimability of Linear Predictions.

    Provides tools for determining estimability of linear functions of
    regression coefficients, and 'epredict' methods that handle non-estimable
    cases correctly. Estimability theory is discussed in many linear-models
    textbooks including Chapter 3 of Monahan, JF (2008), "A Primer on Linear
    Models", Chapman and Hall (ISBN 978-1-4200-6201-4)."""

    cran = "estimability"

    version("1.4.1", sha256="c65aaf1e452f3947013d3ce05ae674d48492081f615a942592dc91db780f1124")
    version("1.3", sha256="a33179c5fbd6a1a623d90cb6f1743148f92c09429fac466867f3ea70946a2e32")
