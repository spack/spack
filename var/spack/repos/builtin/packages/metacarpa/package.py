# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.boost import Boost
from spack.package import *


class Metacarpa(MakefilePackage):
    """
    METACARPA is designed for meta-analysing genetic association studies with overlapping or related samples, 
    when details of the overlap or relatedness are unknown. 
    It implements and expands a method first described by Province and Borecki.
    """

    homepage = "https://www.sanger.ac.uk/tool/metacarpa/"
    url = "https://github.com/hmgu-itg/metacarpa/archive/refs/tags/1.0.1.tar.gz"

    """
    This software is open source. You are free to fork and modify the software, provided you give credit to the original author.
    
    If you make use of this software in your research please cite as follows : Southam L., Gilly A., Whole genome sequencing and imputation in isolated populations identify genetic associations withmedically-relevant complex traits. Nat Commun. 2017 May 26;8:15606. doi: 10.1038/ncomms15606.
    
    I am not sure the specific license this would be as I could not find it anywhere.
    """

    version("1.0.1", sha256="7d8fc774a88bf75a53ef8f74462924abba9b99fccbaa9979654c01e4379fab91")

    depends_on("boost@1.60.0")
    depends_on(Boost.with_default_variants)
    depends_on("cmake")
    build_system = "Makefile"
    build_directory = "src"

    def edit(self, spec, prefix):
        makefile = FileFilter("src/Makefile")
        makefile.filter(r"^IDIR.*", "IDIR=" + spec["boost"].prefix.include)
        makefile.filter(r"^LDIR.*", "LDIR=" + spec["boost"].prefix.lib)

    def install(self, spec, prefix):
        mkdirp(prefix.src)
        install_tree("src",prefix.src)
        mkdirp(prefix.bin)
        install("src/metacarpa",prefix.bin)


