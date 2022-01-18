# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Imgui(Package):
    """Dear ImGui is a bloat-free graphical user interface library for C++.

    It outputs optimized vertex buffers that you can render anytime in your 3D-pipeline
    enabled application. It is fast, portable, renderer agnostic and self-contained
    (no external dependencies)."""

    homepage = "https://github.com/ocornut/imgui"
    url      = "https://github.com/ocornut/imgui/archive/refs/tags/v1.85.tar.gz"

    version('1.85', sha256='7ed49d1f4573004fa725a70642aaddd3e06bb57fcfe1c1a49ac6574a3e895a77')

    def install(self, spec, prefix):
        # No specific build process is required.
        # You can add the .cpp files to your existing project.
        install_tree('.', prefix)
