# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PyCrsim(PythonPackage):
    """With the emergence of versatile storage systems, multi-level checkpointing (MLC)
    has become a common approach to gain efficiency. However, multi-level checkpoint/restart can
    cause enormous I/O traffic on HPC systems. To use multilevel checkpointing efficiently,
    it is important to optimize check-point/restart configurations.
    Current approaches, namely modeling and simulation, are either inaccurate or slow in
    determining the optimal configuration for a large scale system.
    In this paper, we show that machine learning models can be used in combination with
    accurate simulation to determine the optimal checkpoint configurations.
    We also demonstrate that more advanced techniques such as neural networks can further improve
    the performance in optimizing checkpoint configurations. """

    homepage = "https://github.com/kento/CRSim"
    url      = "https://github.com/kento/CRSim/archive/refs/heads/main.tar.gz"


    version('1.0.0', sha256='fcb014ad70ad905d0568388cc5fa76c592b3476b4a21a11f1d2489442a57cabc')

    depends_on('python@3.6', type=('build', 'run'))

    phases = ["install"]


    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(join_path(self.stage.source_path, "src", "*"), prefix.bin)
        filter_file(r'#!/bin/python', '#!/usr/bin/env python3', prefix.bin.CRtool)
