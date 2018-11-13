# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlYamlLibyaml(PerlPackage):
    """Perl YAML Serialization using XS and libyaml  """

    homepage = "http://search.cpan.org/~tinita/YAML-LibYAML/"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/YAML-LibYAML-0.67.tar.gz"

    version('0.67', '5a787150db680e3ab3f753f2e54640ab')
