# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openfst(AutotoolsPackage):
    """OpenFst is a library for constructing, combining, optimizing,
        and searching weighted finite-state transducers (FSTs). Weighted
        finite-state transducers are automata where each transition has
        an input label, an output label, and a weight."""

    homepage = "http://www.openfst.org"
    url      = "http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.1.tar.gz"
    list_url = "http://www.openfst.org/twiki/bin/view/FST/FstDownload"

    version('1.6.1',  '1173066ed987072183b950b54bdc9315')
    version('1.6.0',  '2b7bcfde6b629857dc5f9ad7edd6ece9')
    version('1.5.4',  'e52bd59ec9d9edde0c1268a382662741')
    version('1.5.3',  'f04e580b5bc574571854304c9656a3e2')
    version('1.5.2',  'e9d43874f7cadf791394caab3925eee4')
    version('1.5.1',  '8869e44c5a4af65409ae78b9f482b40e')
    version('1.5.0',  'a24fee5ffe28744c6fb7b1a49e0006c4')
    version('1.4.1-patch',  'ca8f1730b9b9b281e515611fa9ae23c0',
            url='http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.4.1.tar.gz')
    version('1.4.1',  'ca8f1730b9b9b281e515611fa9ae23c0')
    version('1.4.0',  '662367ec91084ffab48ee9b5716de39c')

    conflicts('%intel@16:')
    conflicts('%gcc@6:')

    variant('far', default=False, description="Enable FAR support")

    # Patch openfst-1.4.1 for kaldi@c024e8
    # See https://github.com/kaldi-asr/kaldi/blob/c024e8aa0a727bf76c91a318f76a1f8b0b59249e/tools/Makefile#L82-L88
    patch('openfst-1.4.1.patch', when='@1.4.1-patch')
    patch('openfst_gcc41up.patch', when='@1.4.1-patch')

    def configure_args(self):
        args = []
        spec = self.spec
        if '+far' in spec:
            args.append('--enable-far')
        else:
            args.append('--disable-far')
        return args
