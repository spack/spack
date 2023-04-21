# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xcrysden(Package):
    """XCrySDen is a crystalline and molecular structure visualisation program aiming 
    at display of isosurfaces and contours, which can be superimposed on crystalline 
    structures and interactively rotated and manipulated. It runs on GNU/Linux."""

    homepage = "http://www.xcrysden.org/"
    url = "http://www.xcrysden.org/download/xcrysden-1.6.2.tar.gz"

    version("1.6.3-rc2-bin-shared", sha256="4d05dec489e2f94de29c784238b72f6bf86622703627cdc460e552fa120dbc69")
    version("1.6.3-rc2", sha256="0565f55dfb67c73a824569bd2f02875f1e15c7214b86736fce4cacc3f5a189fe")
    version("1.6.3-rc1", sha256="dac69eb6c37a64cb26e8e0fb378698786df61109ceea364f3878f0cbbe28c966")
    version("1.6.2-windows-wsl", sha256="e26be2ab70530b500694ef23dfcbec3b1e4bef13248cb0833bea9c2b94a955f4")
    version("1.6.2-macosx-shared", sha256="f452b4eaac5b079f999761eb390610db898cad54d5cf82e8058aecf49449c1ae")
    version("1.6.2-macosx-semishared", sha256="525f0c1b5b2d128edff7d572548a51a96682dcf33d0918338fe2efdb9ac9f0b4")
    version("1.6.2-cyg", sha256="609d7779fd14d5aac05332da012a34e3795a586a7d232621ce043ab1e6f103a4")
    version("1.6.2", sha256="811736ee598bec1a5b427fd10e4e063a30dd7cadae96a43a50b36ce90a4f503f")
    version("1.6.1", sha256="8a9c6d83c4a9e189dbb977a04ccf1b260871e945afdf1ca75830616a6cb442c5")
    version("1.6.0-rc3", sha256="8a41d4ac45da77e2885dba55a55ba5dd0dab79cce90dd3e147ceed937917a754")
    version("1.6.0-rc2", sha256="063ffc4775b3ac5f93b41ee554242dd09577a910968a53468a8077b547769054")
    version("1.6.0-rc1", sha256="f1368d7eda680013c025f77b5f97185e0a7d9862abc56e083b077b115aadd170")
    version("1.6.0-bin-shared", sha256="ffc36561ffc61b97388756d4a1120ef77d6987e015d2a8d0c404c4ff37ab9aa5")
    version("1.6.0", sha256="9ee1d9a1113c72722f0c7c6e08e70a568b6ee7a2f81a25ac636f46b16741b0b6")
    version("1.5.60-cyg", sha256="ac1f2102abba9bc66f642be8d3b07f644612524219d4c99441f1c8b88b0a6457")
    version("1.5.60", sha256="a695729f1bb3e486b86a74106c06a392c8aca048dc6b0f20785c3c311cfb2ef4")
    version("1.5.53-cyg", sha256="b680ef6bf435495827d28b55f2c01fe88becc2d003d6a3da446e160330204d71")
    version("1.5.53", sha256="9eff395b63a3490e8bbb7d8c8501d1ecf3e1157897eb066baae7fcaf7f0788be")


    def install(self, spec, prefix):
        make()
        make("install")
