# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand

resource = SpackCommand('resource')

#: these are hashes used in mock packages
mock_hashes = [
    'abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234',
    '1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd',
    'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c',
    'c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8',
    '24eceabef5fe8f575ff4b438313dc3e7b30f6a2d1c78841fbbe3b9293a589277',
    '689b8f9b32cb1d2f9271d29ea3fca2e1de5df665e121fca14e1364b711450deb',
    'ebe27f9930b99ebd8761ed2db3ea365142d0bafd78317efb4baadf62c7bf94d0',
    '208fcfb50e5a965d5757d151b675ca4af4ce2dfd56401721b6168fae60ab798f',
    'bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c',
    '7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730',
]


def test_resource_list(mock_packages, capfd):
    with capfd.disabled():
        out = resource('list')

    for h in mock_hashes:
        assert h in out

    assert 'url:' in out
    assert 'applies to:' in out
    assert 'patched by:' in out
    assert 'path:' in out

    assert 'repos/builtin.mock/packages/patch-a-dependency/libelf.patch' in out
    assert 'applies to: builtin.mock.libelf' in out
    assert 'patched by: builtin.mock.patch-a-dependency' in out


def test_resource_list_only_hashes(mock_packages, capfd):
    with capfd.disabled():
        out = resource('list', '--only-hashes')

    for h in mock_hashes:
        assert h in out


def test_resource_show(mock_packages, capfd):
    with capfd.disabled():
        out = resource('show', 'c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8')

    assert out.startswith('c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8')
    assert 'repos/builtin.mock/packages/patch-a-dependency/libelf.patch' in out
    assert 'applies to: builtin.mock.libelf' in out
    assert 'patched by: builtin.mock.patch-a-dependency' in out

    assert len(out.strip().split('\n')) == 4
