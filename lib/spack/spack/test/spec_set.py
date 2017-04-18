##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest

from spack.spec import Spec
from spack.schema import FileFormatError
from spack.util.spec_set import CombinatorialSpecSet


pytestmark = pytest.mark.usefixtures('config')


basic_yaml_file = {
    'test-suite': {
        'include': ['gmake'],
        'matrix': [
            {'packages': {
                'gmake': {
                    'versions': ['4.0']
                }
            }},
            {'compilers': {
                'gcc': {
                    'versions': ['4.2.1', '6.3.0']
                }, 'clang': {
                    'versions': ['8.0', '3.8']
                }
            }},
        ]
    }
}


def test_spec_set_basic():
    spec_set = CombinatorialSpecSet(basic_yaml_file, False)
    specs = list(spec for spec in spec_set)
    assert len(specs) == 4


def test_spec_set_no_include():
    yaml_file = {
        'test-suite': {
            'matrix': [
                {'packages': {
                    'gmake': {
                        'versions': ['4.0']
                    }
                }},
                {'compilers': {
                    'gcc': {
                        'versions': ['4.2.1', '6.3.0']
                    }, 'clang': {
                        'versions': ['8.0', '3.8']
                    }
                }},
            ]
        }
    }
    spec_set = CombinatorialSpecSet(yaml_file, False)
    specs = list(spec for spec in spec_set)
    assert len(specs) == 4


def test_spec_set_exclude():
    yaml_file = {
        'test-suite': {
            'include': ['gmake'],
            'exclude': ['gmake'],
            'matrix': [
                {'packages': {
                    'gmake': {
                        'versions': ['4.0']
                    }
                }},
                {'compilers': {
                    'gcc': {
                        'versions': ['4.2.1', '6.3.0']
                    }, 'clang': {
                        'versions': ['8.0', '3.8']
                    }
                }},
            ]
        }
    }
    spec_set = CombinatorialSpecSet(yaml_file, False)
    specs = list(spec for spec in spec_set)
    assert len(specs) == 0


def test_spec_set_include_limited_packages():
    yaml_file = {
        'test-suite': {
            'include': ['gmake'],
            'matrix': [
                {'packages': {
                    'gmake': {
                        'versions': ['4.0']
                    },
                    'appres': {
                        'versions': ['1.0.4']
                    },
                    'allinea-reports': {
                        'versions': ['6.0.4']
                    }
                }},
                {'compilers': {
                    'gcc': {
                        'versions': ['4.2.1', '6.3.0']
                    }, 'clang': {
                        'versions': ['8.0', '3.8']
                    }
                }},
            ]
        }
    }
    spec_set = CombinatorialSpecSet(yaml_file, False)
    specs = list(spec for spec in spec_set)
    assert len(specs) == 4


def test_spec_set_simple_spec_list():
    yaml_file = {
        'test-suite': {
            'matrix': [
                {'specs': [
                    'gmake@4.0',
                    'appres@1.0.4',
                    'allinea-reports@6.0.4'
                ]},
            ]
        }
    }
    spec_set = CombinatorialSpecSet(yaml_file, False)
    specs = list(spec for spec in spec_set)
    assert len(specs) == 3


def test_spec_set_with_specs():
    yaml_file = {
        'test-suite': {
            'include': ['gmake', 'appres'],
            'matrix': [
                {'specs': [
                    'gmake@4.0',
                    'appres@1.0.4',
                    'allinea-reports@6.0.4'
                ]},
                {'compilers': {
                    'gcc': {
                        'versions': ['4.2.1', '6.3.0']
                    }, 'clang': {
                        'versions': ['8.0', '3.8']
                    }
                }},
            ]
        }
    }
    spec_set = CombinatorialSpecSet(yaml_file, False)
    specs = list(spec for spec in spec_set)
    assert len(specs) == 8


def test_spec_set_compilers_bad_property():
    yaml_file = {
        'test-suite': {
            'foobar': ['gmake'],
            'matrix': [
                {'packages': {
                    'gmake': {'versions': ['4.0']},
                }},
                {'compilers': {
                    'gcc': {'versions': ['4.2.1', '6.3.0']},
                    'clang': {'versions': ['8.0', '3.8']},
                }},
            ]
        }
    }
    with pytest.raises(FileFormatError):
        CombinatorialSpecSet(yaml_file)


def test_spec_set_packages_no_matrix():
    yaml_file = {
        'test-suite': {
            'include': ['gmake'],
            'packages': {
                'gmake': {
                    'versions': ['4.0']
                },
                'appres': {
                    'versions': ['1.0.4']
                },
                'allinea-reports': {
                    'versions': ['6.0.4']
                }
            },
        }
    }
    with pytest.raises(FileFormatError):
        CombinatorialSpecSet(yaml_file)


def test_spec_set_get_cdash_string():
    yaml_file = {
        'test-suite': {
            'cdash': 'http://example.com/cdash',
            'project': 'testproj',
            'matrix': [
                {'packages': {
                    'gmake': {'versions': ['4.0']},
                }},
                {'compilers': {
                    'gcc': {'versions': ['4.2.1', '6.3.0']},
                    'clang': {'versions': ['8.0', '3.8']},
                }},
            ]
        }
    }

    spec_set = CombinatorialSpecSet(yaml_file)
    assert spec_set.cdash == ['http://example.com/cdash']
    assert spec_set.project == 'testproj'


def test_spec_set_get_cdash_array():
    yaml_file = {
        'test-suite': {
            'cdash': ['http://example.com/cdash', 'http://example.com/cdash2'],
            'project': 'testproj',
            'matrix': [
                {'packages': {
                    'gmake': {'versions': ['4.0']},
                }},
                {'compilers': {
                    'gcc': {'versions': ['4.2.1', '6.3.0']},
                    'clang': {'versions': ['8.0', '3.8']},
                }},
            ]
        }
    }

    spec_set = CombinatorialSpecSet(yaml_file)
    assert spec_set.cdash == [
        'http://example.com/cdash', 'http://example.com/cdash2']
    assert spec_set.project == 'testproj'


def test_compiler_specs():
    spec_set = CombinatorialSpecSet(basic_yaml_file, False)
    compilers = spec_set._compiler_specs({
        'gcc': {
            'versions': ['4.2.1', '6.3.0']
        }, 'clang': {
            'versions': ['8.0', '3.8']
        }})

    assert Spec('%gcc@4.2.1') in compilers
    assert Spec('%gcc@6.3.0') in compilers
    assert Spec('%clang@8.0') in compilers
    assert Spec('%clang@3.8') in compilers


def test_package_specs():
    spec_set = CombinatorialSpecSet(basic_yaml_file, False)

    packages = spec_set._package_specs({
        'gmake': {
            'versions': ['4.0', '5.0']
        },
        'appres': {
            'versions': ['1.0.4']
        },
        'allinea-reports': {
            'versions': ['6.0.1', '6.0.3', '6.0.4']
        }
    })

    assert Spec('gmake@4.0') in packages
    assert Spec('gmake@5.0') in packages
    assert Spec('appres@1.0.4') in packages
    assert Spec('allinea-reports@6.0.1') in packages
    assert Spec('allinea-reports@6.0.3') in packages
    assert Spec('allinea-reports@6.0.4') in packages
