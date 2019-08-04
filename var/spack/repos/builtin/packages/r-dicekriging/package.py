# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDicekriging(RPackage):
    """Estimation, validation and prediction of kriging models. Important
       functions : km, print.km, plot.km, predict.km."""

    homepage = "http://dice.emse.fr/"
    url      = "https://cloud.r-project.org/src/contrib/DiceKriging_1.5.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DiceKriging"

    version('1.5.6', sha256='25466d2db9f17083d1c7b9545e5ec88f630be934f9373c2f7b36c38de4e64e92')
    version('1.5.5', 'ee3e2d7a91d4a712467ef4f0b69c2844')
