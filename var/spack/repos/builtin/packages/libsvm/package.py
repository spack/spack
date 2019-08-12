# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsvm(MakefilePackage):
    """Libsvm is a simple, easy-to-use, and efficient software for SVM
       classification and regression."""

    homepage = "https://www.csie.ntu.edu.tw/~cjlin/libsvm/"
    url      = "https://github.com/cjlin1/libsvm/archive/v322.tar.gz"

    version('322', 'd9617d29efad013573f63ca9a517f490')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install('svm-predict', prefix.bin)
        install('svm-scale', prefix.bin)
        install('svm-train', prefix.bin)
        install('svm.o', prefix.lib)
