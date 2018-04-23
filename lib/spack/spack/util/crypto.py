##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import sys
import hashlib

import llnl.util.tty as tty


"""Set of acceptable hashes that Spack will use."""
_hash_algorithms = [
    'md5',
    'sha1',
    'sha224',
    'sha256',
    'sha384',
    'sha512']


_deprecated_hash_algorithms = ['md5']


hashes = dict()


"""Index for looking up hasher for a digest."""
_size_to_hash = dict()


class DeprecatedHash(object):
    def __init__(self, hash_alg, alert_fn, disable_security_check):
        self.hash_alg = hash_alg
        self.alert_fn = alert_fn
        self.disable_security_check = disable_security_check

    def __call__(self, disable_alert=False):
        if not disable_alert:
            self.alert_fn("Deprecation warning: {0} checksums will not be"
                          " supported in future Spack releases."
                          .format(self.hash_alg))
        if self.disable_security_check:
            return hashlib.new(self.hash_alg, usedforsecurity=False)
        else:
            return hashlib.new(self.hash_alg)


for h in _hash_algorithms:
    try:
        if h in _deprecated_hash_algorithms:
            hash_gen = DeprecatedHash(
                h, tty.debug, disable_security_check=False)
            _size_to_hash[hash_gen(disable_alert=True).digest_size] = hash_gen
        else:
            hash_gen = getattr(hashlib, h)
            _size_to_hash[hash_gen().digest_size] = hash_gen
        hashes[h] = hash_gen
    except ValueError:
        # Some systems may support the 'usedforsecurity' option so try with
        # that (but display a warning when it is used)
        hash_gen = DeprecatedHash(h, tty.warn, disable_security_check=True)
        hashes[h] = hash_gen
        _size_to_hash[hash_gen(disable_alert=True).digest_size] = hash_gen


def checksum(hashlib_algo, filename, **kwargs):
    """Returns a hex digest of the filename generated using an
       algorithm from hashlib.
    """
    block_size = kwargs.get('block_size', 2**20)
    hasher = hashlib_algo()
    with open(filename, 'rb') as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


class Checker(object):
    """A checker checks files against one particular hex digest.
       It will automatically determine what hashing algorithm
       to used based on the length of the digest it's initialized
       with.  e.g., if the digest is 32 hex characters long this will
       use md5.

       Example: know your tarball should hash to 'abc123'.  You want
       to check files against this.  You would use this class like so::

          hexdigest = 'abc123'
          checker = Checker(hexdigest)
          success = checker.check('downloaded.tar.gz')

       After the call to check, the actual checksum is available in
       checker.sum, in case it's needed for error output.

       You can trade read performance and memory usage by
       adjusting the block_size optional arg.  By default it's
       a 1MB (2**20 bytes) buffer.
    """

    def __init__(self, hexdigest, **kwargs):
        self.block_size = kwargs.get('block_size', 2**20)
        self.hexdigest = hexdigest
        self.sum       = None

        bytes = len(hexdigest) / 2
        if bytes not in _size_to_hash:
            raise ValueError(
                'Spack knows no hash algorithm for this digest: %s'
                % hexdigest)

        self.hash_fun = _size_to_hash[bytes]

    @property
    def hash_name(self):
        """Get the name of the hash function this Checker is using."""
        return self.hash_fun().name

    def check(self, filename):
        """Read the file with the specified name and check its checksum
           against self.hexdigest.  Return True if they match, False
           otherwise.  Actual checksum is stored in self.sum.
        """
        self.sum = checksum(
            self.hash_fun, filename, block_size=self.block_size)
        return self.sum == self.hexdigest


def prefix_bits(byte_array, bits):
    """Return the first <bits> bits of a byte array as an integer."""
    if sys.version_info < (3,):
        b2i = ord          # In Python 2, indexing byte_array gives str
    else:
        b2i = lambda b: b  # In Python 3, indexing byte_array gives int

    result = 0
    n = 0
    for i, b in enumerate(byte_array):
        n += 8
        result = (result << 8) | b2i(b)
        if n >= bits:
            break

    result >>= (n - bits)
    return result


def bit_length(num):
    """Number of bits required to represent an integer in binary."""
    s = bin(num)
    s = s.lstrip('-0b')
    return len(s)
