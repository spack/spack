# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIsodate(PythonPackage):
    """This module implements ISO 8601 date, time and duration parsing. The
    implementation follows ISO8601:2004 standard, and implements only date/time
    representations mentioned in the standard. If something is not mentioned
    there, then it is treated as non existent, and not as an allowed option.

    For instance, ISO8601:2004 never mentions 2 digit years. So, it is not
    intended by this module to support 2 digit years. (while it may still be
    valid as ISO date, because it is not explicitly forbidden.) Another example
    is, when no time zone information is given for a time, then it should be
    interpreted as local time, and not UTC.

    As this module maps ISO 8601 dates/times to standard Python data types,
    like date, time, datetime and timedelta, it is not possible to convert all
    possible ISO 8601 dates/times. For instance, dates before 0001-01-01 are
    not allowed by the Python date and datetime classes. Additionally
    fractional seconds are limited to microseconds. That means if the parser
    finds for instance nanoseconds it will round it to microseconds."""

    homepage = "https://github.com/gweis/isodate/"
    url      = "https://pypi.io/packages/source/i/isodate/isodate-0.6.0.tar.gz"

    version('0.6.0', sha256='2e364a3d5759479cdb2d37cce6b9376ea504db2ff90252a2e5b7cc89cc9ff2d8')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
