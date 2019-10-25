# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install osqp
#
# You can edit this file again by typing:
#
#     spack edit osqp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Osqp(CMakePackage):
    """
    The OSQP (Operator Splitting Quadratic Program) solver is a numerical
    optimization package for solving problems in the form:
     minimize        0.5 x' P x + q' x, and
     subject to      l <= A x <= u,
    where `x in R^n` is the optimization variable.
    """

    homepage = "https://osqp.org"
    git      = "https://github.com/oxfordcontrol/osqp.git"

    version('master', branch='master', submodules=True)
    version('0.6.0', commit='0baddd36bd57ec1cace0a52c6dd9663e8f16df0a', submodules=True, preferred=True)
    version('0.5.0', commit='97050184aa2cbebe446ae02d1f8b811243e180d6', submodules=True)
