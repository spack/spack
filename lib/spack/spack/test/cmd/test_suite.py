##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
import spack.cmd.test_suite as test_suite
import datetime
import os
import shutil


@pytest.mark.usefixtures('config')
class TestCompilers(object):

    yaml_file = {'test-suite':
                 {'project': 'test',
                     'include': ['gmake'],
                     'cdash': ['https://spack.io/cdash'],
                     'packages': {
                         'gmake': {
                             'versions': [4.0]
                         }
                     },
                     'compilers': {
                         'gcc': {
                             'versions': ['4.2.1', '6.3.0']
                         }, 'clang': {
                             'versions': [8.0, 3.8]
                         }
                     }
                  }
                 }

    yaml_file_no_include = {'test-suite':
                            {'project': 'test',
                             'cdash': ['https://spack.io/cdash'],
                             'packages': {
                                 'gmake': {
                                     'versions': [4.0]
                                 }
                             },
                                'compilers': {
                                 'gcc': {
                                     'versions': ['4.2.1', '6.3.0']
                                 }, 'clang': {
                                     'versions': [8.0, 3.8]
                                 }
                             }
                             }
                            }

    yaml_file_exclude = {'test-suite':
                         {'project': 'test',
                          'include': ['gmake'],
                          'exclude': ['gmake'],
                          'cdash': ['https://spack.io/cdash'],
                          'packages': {
                              'gmake': {
                                  'versions': [4.0]
                              }
                          },
                             'compilers': {
                              'gcc': {
                                  'versions': ['4.2.1', '6.3.0']
                              }, 'clang': {
                                  'versions': [8.0, 3.8]
                              }
                          }
                          }
                         }

    yaml_file_limited_packages = {'test-suite':
                                  {'project': 'test',
                                   'include': ['gmake'],
                                   'cdash': ['https://spack.io/cdash'],
                                   'packages': {
                                       'gmake': {
                                           'versions': [4.0]
                                       },
                                       'appres': {
                                           'versions': ['1.0.4']
                                       },
                                       'allinea-reports': {
                                           'versions': ['6.0.4']
                                       }
                                   },
                                      'compilers': {
                                       'gcc': {
                                           'versions': ['4.2.1', '6.3.0']
                                       }, 'clang': {
                                           'versions': [8.0, 3.8]
                                       }
                                   }
                                   }
                                  }

    yaml_file_no_project = {'test-suite':
                            {'include': ['gmake'],
                             'cdash': ['https://spack.io/cdash'],
                             'packages': {
                                'gmake': {
                                    'versions': [4.0]
                                },
                                'appres': {
                                    'versions': ['1.0.4']
                                },
                                'allinea-reports': {
                                    'versions': ['6.0.4']
                                }
                            },
                                'compilers': {
                                'gcc': {
                                    'versions': ['4.2.1', '6.3.0']
                                }, 'clang': {
                                    'versions': [8.0, 3.8]
                                }
                            }
                            }
                            }

    yaml_file_no_cdash = {'test-suite':
                          {'include': ['gmake'],
                           'packages': {
                              'gmake': {
                                  'versions': [4.0]
                              },
                              'appres': {
                                  'versions': ['1.0.4']
                              },
                              'allinea-reports': {
                                  'versions': ['6.0.4']
                              }
                          },
                              'compilers': {
                              'gcc': {
                                  'versions': ['4.2.1', '6.3.0']
                              }, 'clang': {
                                  'versions': [8.0, 3.8]
                              }
                          }
                          }
                          }

    def test_create_tests(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        test_output = ts.create_tests(self.yaml_file, True)
        assert len(test_output['tests']) == 4

    def test_create_tests_no_include(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        test_output = ts.create_tests(self.yaml_file_no_include, True)
        assert len(test_output['tests']) == 4

    def test_create_tests_exclude(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        test_output = ts.create_tests(self.yaml_file_exclude, True)
        assert len(test_output['tests']) == 0

    def test_create_tests_include_limited_packages(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        test_output = ts.create_tests(self.yaml_file_limited_packages, True)
        assert len(test_output['tests']) == 4

    def test_create_tests_no_project(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        test_output = ts.create_tests(self.yaml_file_no_project, True)
        assert len(test_output['tests']) == 4

    def test_create_tests_no_cdash(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        test_output = ts.create_tests(self.yaml_file_no_cdash, True)
        assert "cdash" not in test_output

    def test_return_valid_yaml_files(self):
        # create fake yaml file
        test_files = []
        test_files.append(os.getcwd() + "/test3.yaml")
        for file in test_files:
            if not os.path.exists(file):
                open(file, "a")
                # os.mkdirs(os.path.dirname(files))
        assert len(test_suite.return_valid_yaml_files(test_files)) == 1
        for file in test_files:
            os.remove(file)  # will remove a test file.
            assert not os.path.exists(file)

    def test_return_valid_yaml_file_list(self):
        # create fake yaml file
        test_files = []
        test_files.append(os.getcwd() + "/test2.txt")
        test_files.append(os.getcwd() + "/test2.yaml")
        for file in test_files:
            if not os.path.exists(file):
                open(file, "a")
                # os.mkdirs(os.path.dirname(files))
        assert len(test_suite.return_valid_yaml_files(test_files)) == 1
        for file in test_files:
            os.remove(file)  # will remove a test file.
            assert not os.path.exists(file)

    def test_filename(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        assert "test.yaml" in ts.yaml_file

    def test_combinatorial(self):
        combinations = []
        compiler = "gcc"
        versions = ["4.2.1", "6.3.0"]
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        [combinations.append(spec)
         for spec in ts.combinatorial(compiler, versions)]
        assert len(combinations) == 2

    def test_combinatorial_compiler(self):
        combinations = []
        compiler_version = ["gcc@4.2.1", "gcc@6.3.0"]
        package_versions = ["bzip2@1.2.3", "libelf@3.4"]
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        [combinations.append(spec)
         for spec in ts.combinatorial_compiler(
            compiler_version, package_versions)]
        assert len(combinations) == 4

    def test_create_path(self):
        test_suite.create_path()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        path = os.getcwd() + "/spack-test-" + str(timestamp) + "/"
        assert os.path.exists(path)
        shutil.rmtree(path)
        assert not os.path.exists(path)
