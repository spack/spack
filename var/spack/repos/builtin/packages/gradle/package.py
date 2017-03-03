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
from spack import *
from distutils.dir_util import copy_tree


class Gradle(Package):
    """Gradle is an open source build automation system that builds 
    upon the concepts of Apache Ant and Apache Maven and introduces 
    a Groovy-based domain-specific language (DSL) instead of the XML 
    form used by Apache Maven for declaring the project configuration.
    Gradle uses a directed acyclic graph ("DAG") to determine the 
    order in which tasks can be run."""

    homepage = "https://gradle.org"
    url      = "https://services.gradle.org/distributions/gradle-3.4-all.zip"

    version('3.4',    '5ae23dbd730dea22eb79cd97a072f06a')
    version('3.3',    '355f61e9c5d092d49577765ab3712dc0')
    version('3.2.1',  'd44dba900ff364103e1f45c0f4b27bbe')
    version('3.2',    '296cb0e8a94bf72dd80ff7f0ebbf33ed')
    version('3.1',    '21b34a8c6bae67c729b37b4bd59cf9d0')
    version('3.0',    '0a7533599b86909c85b117e897501165')
    version('2.14.1', 'f74b094923ae76f15f138d42373bb4bc')
    version('2.14',   'e069dca1ec042665d61c85caeb4b32ed')
    version('2.13',   '8e7b31a8b8500752c3d80bd683d120c1')
    version('2.12',   '42cce06d8fe3a7125ac9b2a6dcc13927')
    version('2.11',   'd99911cb2d0e86293e1793efc61cd642')
    version('2.10',   'c5d8e57186b60c6d6485682f9907b257')
    version('2.9',    '1ee1a98b9a73c24633c14abf7f2a5189')
    version('2.8',    '9f0e8b0c195d7ea6335a724bc90622a9')
    version('2.7',    '77a77e364c1e2005c62909e6f51a434a')
    version('2.6',    '6947e873602b3668b2f3cd8e2dd228f1')
    version('2.5',    '17295dee02217cbe4f07b0d8bb72c467')
    version('2.4',    'e1528eeca5c66579ebaee4c7c13bec2a')
    version('2.3',    '26c527220d869dbd6bb8cd903dd044e1')
    version('2.2.1',  '1107fbaf94ab7eae26d76d71b5f8db13')
    version('2.2',    '143830aea6bbed4ee77baa3dd191745f')
    version('2.1',    '603c07bc1fa737809ef0d9bc5b11960a')
    version('2.0',    '1d0853b99e6097ea3dea5f3604dc0846')
    version('1.12',   'f957126d8e84d7ee7c859d02c2ae1fc1')
    version('1.11',   '36d2e8f0d5059c815496775af5f688b4')
    version('1.10',   'c7ea1213cee7cf2272c5189dbc6f983b')
    version('1.9',    'cc0a214649b283cc9594b5b82cb84ce5')
    version('1.8',    '1733ee0850618a73b54c9ba407de56b6')
    version('1.5',    '80e60e3b71f1745bbf06f41795ac2908')
    version('1.4',    'cc934cab80bed0caccaa096b83cd4d67')
    version('1.3',    'f6bce3798f4ee184926592e9a6893e0e')
    version('1.2',    'c4741339370bd5e825b2abb9f2cb5b40')
    version('1.1',    'afb37b4b35a30ebd5d758c333c147ce9')
    version('1.0',    '7697cb1e78c7e7362aa422d1790238bd')
    version('0.9.2',  '8574a445267ce3ad21558e300d854d24')
    version('0.9.1',  '8fa0acfbcdf01a8425c1f797f5079e21')
    version('0.9',    '9da1eb9fb32d9c303de5fd5568694634')
    version('0.8',    '73a0ed51b6ec00a7d3a9d242d51aae60')
    version('0.7',    'a8417dbbd62f7013002cb55a44f12cc3')

    depends_on('jdk')

    def install(self, spec, prefix):
        copy_tree('.', prefix)
